from django.http import JsonResponse
from .models import SupervisorProfile, StudentProposal
from .services import calculate_academic_fit
from .algorithms import generate_hybrid_preferences, spa_allocation

def run_allocation_algorithm(request):
    # 1. FETCH DATA FROM DATABASE
    supervisors = list(SupervisorProfile.objects.all())
    students = list(StudentProposal.objects.all())
    
    if not supervisors or not students:
        return JsonResponse({"error": "No data found. Add supervisors and students first."}, status=400)

    # 2. PREPARE DATA FOR AI (Block 1)
    # Extract just the text for SBERT
    student_texts = [s.topic_description for s in students]
    supervisor_texts = [s.research_interests for s in supervisors]
    
    # Extract names and choices for the Algorithms
    supervisor_names = [s.name for s in supervisors]
    student_choices = [s.manual_preferences for s in students]
    
    # Create a capacity dictionary { 'Dr. Smith': 5, ... }
    capacities = {s.name: s.capacity for s in supervisors}

    # 3. RUN THE AI (Service Layer)
    # This calls your SBERT function
    score_matrix = calculate_academic_fit(student_texts, supervisor_texts)

    # 4. GENERATE PREFERENCES (Block 2)
    # This calls your Hybrid List function
    preference_data = generate_hybrid_preferences(
        student_choices, 
        supervisor_names, 
        score_matrix, 
        n_limit=10
    )

    # 5. EXECUTE ALLOCATION (Block 3)
    # This calls your SPA function
    final_matches = spa_allocation(
        preference_data['students'],
        preference_data['supervisors'],
        capacities,
        supervisor_names
    )

    # 6. RETURN RESULTS
    return JsonResponse({
        "status": "success",
        "matches": final_matches,
        "debug_preferences": preference_data # Helpful for seeing what the AI thought
    })