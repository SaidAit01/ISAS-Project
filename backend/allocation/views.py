from django.http import JsonResponse, HttpResponse
from .models import SupervisorProfile, StudentProposal, SystemConfiguration, ProjectCategory, TechnicalSkill, ResearchInterest
from .services import calculate_academic_fit
from .algorithms import generate_hybrid_preferences, spa_allocation
import json 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsProjectCoordinator, IsSupervisor, IsStudent
from django.views.decorators.csrf import csrf_exempt
import csv
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['POST'])
@permission_classes([IsProjectCoordinator])
def run_allocation_algorithm(request):
    supervisors = list(SupervisorProfile.objects.all())
    all_active_students = list(StudentProposal.objects.filter(has_submitted=True))
    pending_students = list(StudentProposal.objects.filter(has_submitted=False))
    pending_names = [s.name for s in pending_students]
    
    if not supervisors or not all_active_students:
        return JsonResponse({"error": "No data found. Add supervisors and students first."}, status=400)

    pre_agreed_students = [s for s in all_active_students if s.has_pre_agreement and s.pre_agreed_supervisor]
    standard_students = [s for s in all_active_students if not (s.has_pre_agreement and s.pre_agreed_supervisor)]

    capacities = {s.name: s.capacity for s in supervisors}
    final_matches = {'matched': {}, 'unallocated': []}
    for sup in supervisors:
        final_matches['matched'][sup.name] = []

    for student in pre_agreed_students:
        sup_name = student.pre_agreed_supervisor.name
        final_matches['matched'][sup_name].append(student.name)
        if capacities[sup_name] > 0:
            capacities[sup_name] -= 1

    preference_data = {} 
    
    if standard_students:
        supervisor_names = [s.name for s in supervisors]
        student_choices = [s.manual_preferences for s in standard_students]
        student_names = [s.name for s in standard_students]

        score_matrix = calculate_academic_fit(standard_students, supervisors)

        preference_data = generate_hybrid_preferences(
            student_choices, 
            supervisor_names, 
            score_matrix, 
            n_limit=10
        )

        student_prefs_dict = {i: prefs for i, prefs in enumerate(preference_data['students'])}
        supervisor_prefs_dict = {i: prefs for i, prefs in enumerate(preference_data['supervisors'])}

        algo_matches = spa_allocation(
            student_prefs_dict,      
            supervisor_prefs_dict,   
            capacities,
            supervisor_names, 
            student_names
        )

        algo_matched = algo_matches.get('matched', {})
        for sup_name, allocated_names in algo_matched.items():
            final_matches['matched'][sup_name].extend(allocated_names)

        unallocated_names = algo_matches.get('unallocated', [])
        for name in unallocated_names:
            student_obj = next((s for s in standard_students if s.name == name), None)
            topic = student_obj.topic_description if student_obj and student_obj.topic_description else "No specific topic provided."
            skills = student_obj.technical_skills if student_obj else []
            project_category = student_obj.project_category if student_obj else [] 
            
            final_matches['unallocated'].append({
                "name": name,
                "topic": topic,
                "skills": skills,
                "category": project_category
            })
                                  
    StudentProposal.objects.update(allocated_supervisor=None)

    print("\n" + "="*50)
    print("🚨 THE DATABASE SAVING LOOP HAS STARTED! 🚨")
    print("="*50 + "\n")

    actual_matches = final_matches.get('matched', {})
    
    for supervisor_name, allocated_student_names in actual_matches.items():
        if not allocated_student_names:
            continue 
            
        try:
            supervisor_obj = SupervisorProfile.objects.get(name=supervisor_name)
            cleaned_student_names = [name.strip() for name in allocated_student_names]
            
            print(f"✅ SAVING TO DB: {cleaned_student_names} -> {supervisor_name}")
            
            StudentProposal.objects.filter(name__in=cleaned_student_names).update(allocated_supervisor=supervisor_obj)
            
        except SupervisorProfile.DoesNotExist:
            print(f"❌ ERROR: Could not find Supervisor named '{supervisor_name}' in the database.")
            continue 

    print("\n" + "="*50)
    print("🏁 FINISHED SAVING TO DATABASE! 🏁")
    print("="*50 + "\n")

    return JsonResponse({
        "status": "success",
        "matches": final_matches,
        "pending": pending_names,
        "debug_preferences": preference_data 
    })


@api_view(['POST'])
@permission_classes([IsStudent])
def add_student_api(request):
    if request.method == 'POST':
        try:
            data = request.data
            word_count = len(data.get('topic', '').split())
            if word_count > 200:
                return JsonResponse({
                    "status": "error", 
                    "message": f"Topic description is too long. Please limit to 200 words (currently {word_count} words)."
                }, status=400)
    
            preferences = data.get('preferences', [])
            
            config = SystemConfiguration.objects.first()
            limit = config.max_manual_preferences if config else 3 
            word_limit = f"{limit} preference{'s' if limit != 1 else ''}" 
            
            if len(preferences) > limit:
                return JsonResponse({
                    "status": "error", 
                    "message": f"Module Leader constraint: You are only allowed a maximum of {word_limit} manual preferences."
                }, status=400)
                
            has_pre_agreement = data.get('has_pre_agreement', False)
            pre_agreed_name = data.get('pre_agreed_supervisor', '')
            pre_agreed_obj = None
            
            if has_pre_agreement and pre_agreed_name:
                try:
                    pre_agreed_obj = SupervisorProfile.objects.get(name=pre_agreed_name)
                except SupervisorProfile.DoesNotExist:
                    pass 

            student, created = StudentProposal.objects.update_or_create(
                name=data.get('name'), 
                defaults={
                    'topic_description': data.get('topic'),
                    'student_research_interests': data.get('interests', []),
                    'technical_skills': data.get('technical_skills', []),
                    'project_category': data.get('project_category', []),
                    'manual_preferences': preferences,
                    'has_submitted': True, 
                    'has_pre_agreement': has_pre_agreement,
                    'pre_agreed_supervisor': pre_agreed_obj, 
                }
            )
            
            action = "created" if created else "updated"
            return JsonResponse({"status": "success", "id": student.id, "action": action})
            
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
            
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)


@api_view(['POST'])
@permission_classes([IsSupervisor])
def add_supervisor_api(request):
    if request.method == 'POST':
        try:
            data = request.data
            
            supervisor, created = SupervisorProfile.objects.update_or_create(
                name=data.get('name'),
                defaults={
                    'research_interests': data.get('research_interests', []),
                    'suggested_projects': data.get('suggested_projects', []), 
                    'required_skills': data.get('required_skills', []),
                    'project_category': data.get('project_category', []),
                   
                }
            )
            
            action = "created" if created else "updated"
            return JsonResponse({"status": "success", "id": supervisor.id, "action": action})
            
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
            
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

@api_view(['GET'])
@permission_classes([IsSupervisor])
def get_supervisor_profile_api(request, supervisor_name):
    if request.method == 'GET':
        try:
            sup = SupervisorProfile.objects.get(name__iexact=supervisor_name)
            return JsonResponse({
                "status": "success",
                "profile": {
                    "name": sup.name,
                    "research_interests": sup.research_interests or [],
                    "suggested_projects": getattr(sup, 'suggested_projects', []),
                    "required_skills": getattr(sup, 'required_skills', []),
                    "project_category": getattr(sup, 'project_category', []),
                    "capacity": sup.capacity
                }
            })
        except SupervisorProfile.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Not found"}, status=404)
            
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_system_config(request):
    if request.method == 'GET':
        config = SystemConfiguration.objects.first()
        limit = config.max_manual_preferences if config else 3 
        return JsonResponse({
            "status": "success", 
            "max_preferences": limit
        })
        
    elif request.method == 'POST':
        if not request.user.groups.filter(name='Project_Coordinator').exists():
            return JsonResponse({"error": "Only Project Coordinators can change settings."}, status=403)
        try:
            data = request.data
            new_limit = int(data.get('max_preferences', 3))
            
            config = SystemConfiguration.objects.first()
            
            if not config:
                config = SystemConfiguration.objects.create(max_manual_preferences=new_limit)
            else:
                config.max_manual_preferences = new_limit
                config.save()
            
            print(f"✅ SETTINGS UPDATED: Max preferences set to {new_limit}")
            
            return JsonResponse({
                "status": "success", 
                "message": f"Global rule updated! Students may now select up to {new_limit} preferences.",
                "max_preferences": new_limit
            })
            
        except Exception as e:
            print(f"❌ SETTINGS ERROR: {str(e)}")
            return JsonResponse({"status": "error", "message": f"Server Error: {str(e)}"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

@api_view(['POST'])
@permission_classes([IsStudent])
def suggest_supervisors_api(request):
    if request.method == 'POST':
        try:
            data = request.data
            
            topic = data.get('topic', '')
            interests = data.get('interests', [])
            
            if not topic and interests:
                interests_string = ", ".join(interests)
                topic = f"I am looking for a project and I am highly interested in researching topics related to {interests_string}."
                
            if not topic:
                 return JsonResponse({"status": "error", "message": "Topic description is required for AI matching."}, status=400)

            dummy_student = StudentProposal(
                name="Temp_Wizard_User",
                topic_description=topic,
                student_research_interests=interests,
            )
            
            supervisors = list(SupervisorProfile.objects.all())
            if not supervisors:
                return JsonResponse({"status": "error", "message": "No supervisors found in database."}, status=400)

            score_matrix = calculate_academic_fit([dummy_student], supervisors)
            student_scores = score_matrix[0]

            scored_supervisors = list(zip(supervisors, student_scores))
            scored_supervisors.sort(key=lambda x: x[1], reverse=True)
            top_3 = scored_supervisors[:3]
            
            suggestions = []
            for sup, score in top_3:
                suggestions.append({
                    "id": sup.id,
                    "name": sup.name,
                    "interests": sup.research_interests,
                    "match_percentage": round(float(score) * 100, 1) 
                })

            return JsonResponse({
                "status": "success", 
                "suggestions": suggestions
            })
            
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
            
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

@api_view(['GET'])
@permission_classes([IsSupervisor])
def get_supervisor_students_api(request, supervisor_name):
    if request.method == 'GET':
        try:
            supervisor = SupervisorProfile.objects.get(name__iexact=supervisor_name)
            
            students = StudentProposal.objects.filter(allocated_supervisor=supervisor)
            
            student_list = []
            for s in students:
                student_list.append({
                    "name": s.name,
                    "topic": s.topic_description,
                    "interests": ", ".join(s.student_research_interests) if s.student_research_interests else "None listed",
                    "skills": ", ".join(s.technical_skills) if s.technical_skills else "None listed",
                    "project_category": ", ".join(s.project_category) if s.project_category else "None listed",
                })
                
            return JsonResponse({
                "status": "success", 
                "supervisor": supervisor.name,
                "students": student_list
            })
            
        except SupervisorProfile.DoesNotExist:
            return JsonResponse({
                "status": "error", 
                "message": f"Could not find a supervisor named '{supervisor_name}'. Please check the spelling."
            }, status=404)
            
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_supervisors_api(request):
    if request.method == 'GET':
        try:
            supervisors = SupervisorProfile.objects.all().order_by('name')
            
            directory = []
            for sup in supervisors:
                directory.append({
                    "id": sup.id,
                    "name": sup.name,
                    "interests": sup.research_interests or [],
                    "suggested_projects": getattr(sup, 'suggested_projects', []),
                    "project_category": getattr(sup, 'project_category', []),
                    "capacity": sup.capacity
                })
                
            return JsonResponse({"status": "success", "supervisors": directory})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
            
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

@api_view(['GET'])
@permission_classes([AllowAny]) 
def get_taxonomies_api(request):
    if request.method == 'GET':
        categories = list(ProjectCategory.objects.values_list('name', flat=True))
        skills = list(TechnicalSkill.objects.values_list('name', flat=True))
        interests = list(ResearchInterest.objects.values_list('name', flat=True))
        
        return JsonResponse({
            "status": "success",
            "categories": categories,
            "skills": skills,
            "interests": interests
        })
    
@api_view(['GET'])
@permission_classes([IsProjectCoordinator])   
def export_allocations_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="final_allocations.csv"'
    
    writer = csv.writer(response)
    
    writer.writerow([
        'Student Name', 
        'Student Proposal', 
        'Technical Skills', 
        'Project Category', 
        'Assigned Supervisor', 
        'Allocation Type'
    ])

    allocated_students = StudentProposal.objects.filter(allocated_supervisor__isnull=False).select_related('allocated_supervisor')

    for student in allocated_students: 
        match_type = "Pre-Agreed" if student.has_pre_agreement else "Algorithmic Decision"
        
        skills_str = ", ".join(student.technical_skills) if student.technical_skills else "None Listed"
        category_str = ", ".join(student.project_category) if student.project_category else "None Listed"

        writer.writerow([
            student.name, 
            student.topic_description, 
            skills_str,
            category_str,
            student.allocated_supervisor.name, 
            match_type
        ])

    return response

@api_view(['POST'])
@permission_classes([IsProjectCoordinator])
def update_supervisor_capacity_api(request):
    """Allows the Project Coordinator to update a supervisor's capacity."""
    if request.method == 'POST':
        try:
            data = request.data
            supervisor_id = data.get('id')
            new_capacity = int(data.get('capacity'))

            supervisor = SupervisorProfile.objects.get(id=supervisor_id)
            supervisor.capacity = new_capacity
            supervisor.save()

            return JsonResponse({
                "status": "success", 
                "message": f"Capacity for {supervisor.name} successfully updated to {new_capacity}."
            })
        except SupervisorProfile.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Supervisor not found."}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
            
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)