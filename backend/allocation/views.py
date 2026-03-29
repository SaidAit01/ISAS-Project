from django.http import JsonResponse
from .models import SupervisorProfile, StudentProposal, SystemConfiguration
from .services import calculate_academic_fit
from .algorithms import generate_hybrid_preferences, spa_allocation
import json 
from django.views.decorators.csrf import csrf_exempt

def run_allocation_algorithm(request):
    #  Fetch Data from the db
    supervisors = list(SupervisorProfile.objects.all())
    students = list(StudentProposal.objects.filter(has_submitted=True))
    #Fetch the ghost students
    pending_students = list(StudentProposal.objects.filter(has_submitted=False))
    pending_names = [s.name for s in pending_students]
    
    if not supervisors or not students:
        return JsonResponse({"error": "No data found. Add supervisors and students first."}, status=400)

    
    # Extract names and choices for the Algorithms
    supervisor_names = [s.name for s in supervisors]
    student_choices = [s.manual_preferences for s in students]
    student_names = [s.name for s in students]
    
    # Create a capacity dictionary { 'Dr. Smith': 5, ... }
    capacities = {s.name: s.capacity for s in supervisors}

   
    # This calls the SBERT function
    score_matrix = calculate_academic_fit(students, supervisors)

   
    # This calls the Hybrid List function
    preference_data = generate_hybrid_preferences(
        student_choices, 
        supervisor_names, 
        score_matrix, 
        n_limit=10
    )

    #We must convert the LISTS into DICTIONARIES before sending to SPA.
    # The 'enumerate' function gives us the ID (0, 1, 2...) for each person.
    
    student_prefs_dict = {i: prefs for i, prefs in enumerate(preference_data['students'])}
    supervisor_prefs_dict = {i: prefs for i, prefs in enumerate(preference_data['supervisors'])}

    # 5. EXECUTE ALLOCATION (Block 3)
    final_matches = spa_allocation(
        student_prefs_dict,      
        supervisor_prefs_dict,   
        capacities,
        supervisor_names, 
        student_names
    )


    return JsonResponse({
        "status": "success",
        "matches": final_matches,
        "pending": pending_names,
        "debug_preferences": preference_data # Helpful for seeing what the AI thought
    })
@csrf_exempt
def add_student_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            word_count = len(data.get('topic', '').split())
            if word_count > 200:
                return JsonResponse({
                "status": "error", 
                "message": f"Topic description is too long. Please limit to 200 words (currently {word_count} words)."
            }, status=400)
    
        
            preferences = data.get('preferences', [])
            
            # 1. FETCH THE GLOBAL RULE
            # We use .first() because it is a Singleton (only one row exists)
            config = SystemConfiguration.objects.first()
            limit = config.max_manual_preferences if config else 3 # Fallback to 3 if DB is empty
            word_limit = f"{limit} preference{'s' if limit != 1 else ''}" # For error message grammar
            
            # 2. ENFORCE THE RULE (The Bouncer)
            if len(preferences) > limit:
                return JsonResponse({
                    "status": "error", 
                    "message": f"Module Leader constraint: You are only allowed a maximum of {word_limit} manual preferences."
                }, status=400)
            
            # 3. IF THEY PASS, SAVE THE STUDENT
            student = StudentProposal.objects.create(
                name=data.get('name'),
                topic_description=data.get('topic'),
                manual_preferences=preferences
            )
            return JsonResponse({"status": "success", "id": student.id})
            
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
            
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)


@csrf_exempt
def add_supervisor_api(request):
    """We add this back too, so you can add supervisors via the frontend later."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            supervisor = SupervisorProfile.objects.create(
                name=data.get('name'),
                research_interests=data.get('interests'),
                capacity=int(data.get('capacity', 1))
            )
            return JsonResponse({"status": "success", "id": supervisor.id})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
            
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

def get_system_config(request):
    """
    API endpoint for the React frontend to fetch global system rules.
    """
    if request.method == 'GET':
        # Fetch the Singleton row
        config = SystemConfiguration.objects.first()
        
        # If the database is empty, default to 3
        limit = config.max_manual_preferences if config else 3 
        
        return JsonResponse({
            "status": "success", 
            "max_preferences": limit
        })
        
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)