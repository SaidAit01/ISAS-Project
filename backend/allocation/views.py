from django.http import JsonResponse
from .models import SupervisorProfile, StudentProposal, SystemConfiguration
from .services import calculate_academic_fit
from .algorithms import generate_hybrid_preferences, spa_allocation
import json 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .permissions import IsProjectCoordinator, IsSupervisor, IsStudent
from django.views.decorators.csrf import csrf_exempt
import csv
from django.http import JsonResponse, HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from .permissions import IsProjectCoordinator


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['POST'])
@permission_classes([IsProjectCoordinator]
def run_allocation_algorithm(request):
    # 1. Fetch Data
    supervisors = list(SupervisorProfile.objects.all())
    all_active_students = list(StudentProposal.objects.filter(has_submitted=True))
    
    # Fetch the ghost students
    pending_students = list(StudentProposal.objects.filter(has_submitted=False))
    pending_names = [s.name for s in pending_students]
    
    if not supervisors or not all_active_students:
        return JsonResponse({"error": "No data found. Add supervisors and students first."}, status=400)

    # ==========================================
    # NEW: THE PRE-AGREEMENT INTERCEPTION
    # ==========================================
    # Separate students into the Priority Lane and the Standard Lane
    pre_agreed_students = [s for s in all_active_students if s.has_pre_agreement and s.pre_agreed_supervisor]
    standard_students = [s for s in all_active_students if not (s.has_pre_agreement and s.pre_agreed_supervisor)]

    # Map out the initial supervisor capacities
    capacities = {s.name: s.capacity for s in supervisors}
    
    # We will build our final results dictionary right away
    final_matches = {'matched': {}, 'unallocated': []}
    for sup in supervisors:
        final_matches['matched'][sup.name] = []

    # Process the Priority Lane directly (Bypass the AI)
    for student in pre_agreed_students:
        sup_name = student.pre_agreed_supervisor.name
        
        # Hard-code them into the results
        final_matches['matched'][sup_name].append(student.name)
        
        # Deduct the capacity so the AI knows this spot is taken!
        if capacities[sup_name] > 0:
            capacities[sup_name] -= 1

    # ==========================================
    # THE STANDARD ALGORITHM EXECUTION
    # ==========================================
    preference_data = {} # Default empty dictionary in case there are no standard students
    
    # Only run the heavy math if there are students left to allocate
    if standard_students:
        supervisor_names = [s.name for s in supervisors]
        student_choices = [s.manual_preferences for s in standard_students]
        student_names = [s.name for s in standard_students]

        # SBERT function
        score_matrix = calculate_academic_fit(standard_students, supervisors)

        # Hybrid List function
        preference_data = generate_hybrid_preferences(
            student_choices, 
            supervisor_names, 
            score_matrix, 
            n_limit=10
        )

        student_prefs_dict = {i: prefs for i, prefs in enumerate(preference_data['students'])}
        supervisor_prefs_dict = {i: prefs for i, prefs in enumerate(preference_data['supervisors'])}

        # EXECUTE ALLOCATION WITH REDUCED CAPACITIES
        algo_matches = spa_allocation(
            student_prefs_dict,      
            supervisor_prefs_dict,   
            capacities,
            supervisor_names, 
            student_names
        )

        # Merge the AI results with our Priority results
        algo_matched = algo_matches.get('matched', {})
        for sup_name, allocated_names in algo_matched.items():
            final_matches['matched'][sup_name].extend(allocated_names)
                
        final_matches['unallocated'].extend(algo_matches.get('unallocated', []))

    # ==========================================
    # PERMANENTLY SAVE TO DATABASE
    # ==========================================
    StudentProposal.objects.update(allocated_supervisor=None)

    print("\n" + "="*50)
    print("🚨 THE DATABASE SAVING LOOP HAS STARTED! 🚨")
    print("="*50 + "\n")

    actual_matches = final_matches.get('matched', {})
    
    for supervisor_name, allocated_student_names in actual_matches.items():
        # If the supervisor got zero students from both lanes, skip them
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
            
            # 1. FETCH THE GLOBAL RULE
            config = SystemConfiguration.objects.first()
            limit = config.max_manual_preferences if config else 3 
            word_limit = f"{limit} preference{'s' if limit != 1 else ''}" 
            
            # 2. ENFORCE THE RULE (The Bouncer)
            if len(preferences) > limit:
                return JsonResponse({
                    "status": "error", 
                    "message": f"Module Leader constraint: You are only allowed a maximum of {word_limit} manual preferences."
                }, status=400)
            
            # 3. THE UPSERT FIX: UPDATE OR CREATE
            # Django looks for this specific 'name'.
            # If found, it overwrites with the 'defaults'. If not, it creates a new record.
            student, created = StudentProposal.objects.update_or_create(
                name=data.get('name'), 
                defaults={
                    'topic_description': data.get('topic'),
                    'student_research_interests': data.get('interests', []),
                    'technical_skills': data.get('technical_skills', []),
                    'primary_project_format': data.get('primary_project_format', []),
                    'manual_preferences': preferences,
                    'has_submitted': True, 
                    'has_pre_agreement': has_pre_agreement,
                    'pre_agreed_supervisor': pre_agreed_obj, 
                }
            )
            
            # We can even tell the frontend whether it was a brand new student or an update!
            action = "created" if created else "updated"
            return JsonResponse({"status": "success", "id": student.id, "action": action})
            
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
            
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

@api_view(['POST'])
@permission_classes([IsSupervisor])
def add_supervisor_api(request):
    """Upsert endpoint for Supervisors to create or update their profile from React."""
    if request.method == 'POST':
        try:
            data = json.requrests.data
            
            # Use update_or_create to prevent duplicates!
            supervisor, created = SupervisorProfile.objects.update_or_create(
                name=data.get('name'),
                defaults={
                    'research_interests': data.get('research_interests', []),
                    # Using .get() gracefully handles if some fields are left blank
                    'suggested_projects': data.get('suggested_projects', []), 
                    'required_skills': data.get('required_skills', []),
                    'primary_project_format': data.get('primary_project_format', []),
                    'capacity': int(data.get('capacity', 1))
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
    """Fetches a supervisor's current profile data to pre-fill the React form."""
    if request.method == 'GET':
        try:
            sup = SupervisorProfile.objects.get(name__iexact=supervisor_name)
            return JsonResponse({
                "status": "success",
                "profile": {
                    "name": sup.name,
                    "research_interests": sup.research_interests or [],
                    # Using getattr as a safety net just in case your model field names differ slightly
                    "suggested_projects": getattr(sup, 'suggested_projects', []),
                    "required_skills": getattr(sup, 'required_skills', []),
                    "primary_project_format": getattr(sup, 'primary_project_format', []),
                    "capacity": sup.capacity
                }
            })
        except SupervisorProfile.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Not found"}, status=404)
            
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_system_config(request):
    """
    API endpoint to fetch or update the global system rules.
    GET: Returns current settings.
    POST: Updates the settings.
    """
    if request.method == 'GET':
        config = SystemConfiguration.objects.first()
        limit = config.max_manual_preferences if config else 3 
        return JsonResponse({
            "status": "success", 
            "max_preferences": limit
        })
        
    elif request.method == 'POST':
        # MANUAL CHECK: Only allow Coordinators to update the settings
        if not request.user.groups.filter(name='Project_Coordinator').exists():
            return JsonResponse({"error": "Only Project Coordinators can change settings."}, status=403)
        try:
            data = json.requests.data
            new_limit = int(data.get('max_preferences', 3))
            
            # BULLETPROOF SINGLETON UPDATE:
            # Grab the very first configuration row, whatever its ID is.
            config = SystemConfiguration.objects.first()
            
            if not config:
                # If the database is completely empty, create one
                config = SystemConfiguration.objects.create(max_manual_preferences=new_limit)
            else:
                # If it exists, update it
                config.max_manual_preferences = new_limit
                config.save()
            
            print(f"✅ SETTINGS UPDATED: Max preferences set to {new_limit}")
            
            return JsonResponse({
                "status": "success", 
                "message": f"Global rule updated! Students may now select up to {new_limit} preferences.",
                "max_preferences": new_limit
            })
            
        except Exception as e:
            # If it fails, print the exact reason to the VS Code terminal!
            print(f"❌ SETTINGS ERROR: {str(e)}")
            return JsonResponse({"status": "error", "message": f"Server Error: {str(e)}"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

@api_view(['POST'])
@permission_classes([IsStudent])
def suggest_supervisors_api(request):
    """
    On-the-fly AI recommendation endpoint for the Two-Stage Wizard.
    Takes raw student text, runs SBERT, and returns top 3 matches without saving to the DB.
    """
    if request.method == 'POST':
        try:
            data = json.reuqest.data
            
            # STEP 1: Extract the incoming text
            topic = data.get('topic', '')
            interests = data.get('interests', [])
            
            # AI Artificial Context Fix
            if not topic and interests:
                interests_string = ", ".join(interests)
                topic = f"I am looking for a project and I am highly interested in researching topics related to {interests_string}."
                
            if not topic:
                 return JsonResponse({"status": "error", "message": "Topic description is required for AI matching."}, status=400)

            # STEP 2: The "In-Memory" Trick (Clean, no extra fields or returns!)
            dummy_student = StudentProposal(
                name="Temp_Wizard_User",
                topic_description=topic,
                student_research_interests=interests,
            )
            
            # STEP 3: Fetch the Supervisors
            supervisors = list(SupervisorProfile.objects.all())
            if not supervisors:
                return JsonResponse({"status": "error", "message": "No supervisors found in database."}, status=400)

            # STEP 4: Run the AI
            score_matrix = calculate_academic_fit([dummy_student], supervisors)
            student_scores = score_matrix[0]

            # STEP 5: Sort and Package the Top 3 Results
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
    """
    Fetches all students permanently allocated to a specific supervisor.
    """
    if request.method == 'GET':
        try:
            # We use __iexact to make it case-insensitive (e.g., "dr. turing" matches "Dr. Turing")
            supervisor = SupervisorProfile.objects.get(name__iexact=supervisor_name)
            
            # Find all students linked to this supervisor
            students = StudentProposal.objects.filter(allocated_supervisor=supervisor)
            
            # Package the data neatly for React
            student_list = []
            for s in students:
                student_list.append({
                    "name": s.name,
                    "topic": s.topic_description,
                    "interests": ", ".join(s.student_research_interests) if s.student_research_interests else "None listed",
                    "skills": ", ".join(s.technicalskills) if s.technical_skills else "None listed",
                    "project_format": ", ".join(s.primary_project_format) if s.primary_project_format else "None listed",
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
    """Fetches a public directory of all available supervisors for the students to browse."""
    if request.method == 'GET':
        try:
            # Fetch all supervisors and order them alphabetically by name
            supervisors = SupervisorProfile.objects.all().order_by('name')
            
            directory = []
            for sup in supervisors:
                directory.append({
                    "id": sup.id,
                    "name": sup.name,
                    "interests": sup.research_interests or [],
                    # Using getattr as a safety net for the new fields we added
                    "suggested_projects": getattr(sup, 'suggested_projects', []),
                    "primary_project_format": getattr(sup, 'primary_project_format', []),
                    "capacity": sup.capacity
                })
                
            return JsonResponse({"status": "success", "supervisors": directory})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
            
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)
    
 @api_view(['GET'])
 @permission_classes([IsProjectCoordinator])   
def export_allocations_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="final_allocations.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Student Name', 'Student Proposal', 'Assigned Supervisor', 'Allocation Type'])

    allocated_students = StudentProposal.objects.filter(allocated_supervisor__isnull=False).select_related('allocated_supervisor')

    for student in allocated_students: 
        match_type = "Pre-Agreed" if student.has_pre_agreement else "Algorithmic Decision"
        writer.writerow([student.name, student.topic_description, student.allocated_supervisor.name, match_type])

    return response
    
    