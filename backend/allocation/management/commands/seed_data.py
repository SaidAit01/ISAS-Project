from django.core.management.base import BaseCommand
from allocation.models import StudentProposal, SupervisorProfile

class Command(BaseCommand):
    help = 'Seeds the database with a Minimum Viable Dataset (MVD) for testing the Hybrid Engine'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Wiping old data...'))
        StudentProposal.objects.all().delete()
        SupervisorProfile.objects.all().delete()

        # --- SUPERVISORS (Strict JSON List Format) ---
        supervisors = [
            SupervisorProfile(
                name="Dr. Turing", 
                research_interests=["Artificial Intelligence", "Machine Learning", "Deep Learning", "Natural Language Processing"], 
                suggested_projects=["Bias detection in LLMs", "Optimising neural network weights"],
                required_skills=["Python", "PyTorch", "Mathematics"],
                suggested_project_categories=["Theoretical Research", "Software Engineering"],
                capacity=3
            ),
            SupervisorProfile(
                name="Dr. Lovelace", 
                research_interests=["Web Development", "React", "User Experience", "Front-End Architecture"], 
                suggested_projects=["Accessible UI for the visually impaired", "React state management optimization"],
                required_skills=["JavaScript", "React", "HTML/CSS"],
                suggested_project_categories=["Software Engineering"],
                capacity=2
            ),
            SupervisorProfile(
                name="Dr. Hopper", 
                research_interests=["Software Engineering", "Compilers", "Legacy Systems", "Java"], 
                suggested_projects=["Automated COBOL refactoring tool", "JVM Garbage Collection Analysis"],
                required_skills=["Java", "C++", "System Architecture"],
                suggested_project_categories=["Theoretical Research", "Software Engineering"],
                capacity=3
            ),
            SupervisorProfile(
                name="Dr. Dijkstra", 
                research_interests=["Algorithms", "Graph Theory", "Network Routing", "Theoretical Computer Science"], 
                suggested_projects=["Optimizing A* Pathfinding", "Quantum limits of Shor's Algorithm"],
                required_skills=["C++", "Mathematics", "Python"],
                suggested_project_categories=["Theoretical Research"],
                capacity=2
            ),
            SupervisorProfile(
                name="Dr. Neumann", 
                research_interests=["Computer Architecture", "Embedded Systems", "IoT", "Hardware Design"], 
                suggested_projects=["Low-power smart agriculture sensors", "Bare-metal C++ for UAVs"],
                required_skills=["C", "C++", "Hardware Design"],
                suggested_project_categories=["Hardware", "Software Engineering"],
                capacity=3
            ),
            SupervisorProfile(
                name="Dr. Shannon", 
                research_interests=["Information Theory", "Cryptography", "Cyber Security", "Blockchain"], 
                suggested_projects=["Zero-knowledge proofs in voting", "Distributed ledger security"],
                required_skills=["Python", "Cryptography", "Mathematics"],
                suggested_project_categories=["Theoretical Research", "Software Engineering"],
                capacity=2
            )
        ]
        SupervisorProfile.objects.bulk_create(supervisors)
        self.stdout.write(self.style.SUCCESS(f'Created {len(supervisors)} Supervisors.'))

        # --- STUDENTS (Strict JSON List Format & Ghost Flag) ---
        students = [
            # Original 6 Submitted Students
            StudentProposal(name="Eleanor Davies", topic_description="CNN for medical diagnostics and AI.", student_research_interests=["Machine Learning", "Healthcare AI"], programming_languages=["Python", "PyTorch"], project_category=["Software Engineering"], manual_preferences=["Dr. Turing", "Dr. Lovelace"], has_submitted=True),
            StudentProposal(name="Charlotte Lewis", topic_description="Hardware design for urban monitoring.", student_research_interests=["Embedded Systems", "IoT"], programming_languages=["C", "C++"], project_category=["Hardware"], manual_preferences=["Dr. Neumann", "Dr. Dijkstra"], has_submitted=True),
            StudentProposal(name="Liam O'Connor", topic_description="Accessibility-first e-commerce platform.", student_research_interests=["Web Development", "UX Design"], programming_languages=["JavaScript", "React"], project_category=["Software Engineering"], manual_preferences=["Dr. Lovelace"], has_submitted=True),
            StudentProposal(name="William Carter", topic_description="Theoretical limits of Shor's algorithm.", student_research_interests=["Quantum Computing", "Cryptography"], programming_languages=["Python", "Mathematics"], project_category=["Theoretical Research"], manual_preferences=["Dr. Dijkstra", "Dr. Shannon"], has_submitted=True),
            StudentProposal(name="Marcus Johnson", topic_description="Vulnerabilities in standard IoT networks.", student_research_interests=["Cyber Security", "Networking"], programming_languages=["Python", "Bash"], project_category=["Software Engineering"], manual_preferences=["Dr. Shannon", "Dr. Neumann"], has_submitted=True),
            StudentProposal(name="Amelia Martin", topic_description="A Java app for system architecture.", student_research_interests=["Java", "Systems"], programming_languages=["Java"], project_category=["Software Engineering"], manual_preferences=[], has_submitted=True),
            
            # THE AI BOTTLENECK (Competing for Turing's 3 slots)
            StudentProposal(name="Sophia Patel", topic_description="NLP models for translation.", student_research_interests=["Natural Language Processing", "AI"], programming_languages=["Python"], project_category=["Theoretical Research"], manual_preferences=["Dr. Turing"], has_submitted=True),
            StudentProposal(name="James Wilson", topic_description="Deep learning for autonomous driving.", student_research_interests=["Deep Learning", "Computer Vision"], programming_languages=["Python", "PyTorch"], project_category=["Software Engineering"], manual_preferences=["Dr. Turing"], has_submitted=True),
            StudentProposal(name="Mia Kim", topic_description="Bias mitigation in generative AI.", student_research_interests=["Artificial Intelligence", "Ethics"], programming_languages=["Python"], project_category=["Theoretical Research"], manual_preferences=["Dr. Turing"], has_submitted=True),
            StudentProposal(name="Lucas Garcia", topic_description="Optimising transformer architectures.", student_research_interests=["Machine Learning", "Algorithms"], programming_languages=["Python", "Mathematics"], project_category=["Theoretical Research"], manual_preferences=["Dr. Turing", "Dr. Dijkstra"], has_submitted=True),
            
            # THE WEB DEV BOTTLENECK (Competing for Lovelace's 2 slots)
            StudentProposal(name="Ava Robinson", topic_description="State management in large React applications.", student_research_interests=["React", "Front-End Architecture"], programming_languages=["JavaScript", "React"], project_category=["Software Engineering"], manual_preferences=["Dr. Lovelace"], has_submitted=True),
            StudentProposal(name="Ethan Wright", topic_description="Micro-frontends using modern JS frameworks.", student_research_interests=["Web Development", "Software Architecture"], programming_languages=["JavaScript", "HTML/CSS"], project_category=["Software Engineering"], manual_preferences=["Dr. Lovelace", "Dr. Hopper"], has_submitted=True),
            StudentProposal(name="Chloe Martinez", topic_description="UX patterns for mobile-first PWA.", student_research_interests=["User Experience", "Web Development"], programming_languages=["JavaScript"], project_category=["Software Engineering"], manual_preferences=["Dr. Lovelace"], has_submitted=True),

            # THE SECURITY/CRYPTO GROUP (Competing for Shannon's 2 slots)
            StudentProposal(name="Noah Clark", topic_description="Zero-knowledge proofs in digital identity.", student_research_interests=["Cryptography", "Blockchain"], programming_languages=["Python", "Mathematics"], project_category=["Theoretical Research"], manual_preferences=["Dr. Shannon", "Dr. Dijkstra"], has_submitted=True),
            StudentProposal(name="Harper Lee", topic_description="Post-quantum cryptography implementations.", student_research_interests=["Cyber Security", "Cryptography"], programming_languages=["C++", "Python"], project_category=["Theoretical Research"], manual_preferences=["Dr. Shannon"], has_submitted=True),

            # THE HARDWARE/C++ GROUP (Competing for Neumann & Dijkstra)
            StudentProposal(name="Benjamin Hall", topic_description="Efficient graph routing on embedded devices.", student_research_interests=["Graph Theory", "Embedded Systems"], programming_languages=["C++", "C"], project_category=["Hardware"], manual_preferences=["Dr. Neumann", "Dr. Dijkstra"], has_submitted=True),
            StudentProposal(name="Evelyn Young", topic_description="Low-power UAV flight controllers.", student_research_interests=["Hardware Design", "IoT"], programming_languages=["C", "C++"], project_category=["Hardware"], manual_preferences=["Dr. Neumann"], has_submitted=True),
            StudentProposal(name="Alexander King", topic_description="A* pathfinding optimisations in C++.", student_research_interests=["Algorithms", "Network Routing"], programming_languages=["C++"], project_category=["Software Engineering"], manual_preferences=["Dr. Dijkstra", "Dr. Hopper"], has_submitted=True),

            # THE JAVA/ENTERPRISE GROUP (Competing for Hopper's 3 slots)
            StudentProposal(name="Grace Scott", topic_description="Modernizing legacy banking infrastructure.", student_research_interests=["Legacy Systems", "System Architecture"], programming_languages=["Java"], project_category=["Software Engineering"], manual_preferences=["Dr. Hopper"], has_submitted=True),
            StudentProposal(name="Daniel Adams", topic_description="Garbage collection heuristics in large JVMs.", student_research_interests=["Compilers", "Java"], programming_languages=["Java", "C++"], project_category=["Theoretical Research"], manual_preferences=["Dr. Hopper", "Dr. Dijkstra"], has_submitted=True),

            # 21. THE GHOST STUDENT (Missed the deadline!)
            StudentProposal(name="Oliver Brown", topic_description="", student_research_interests=[], programming_languages=[], project_category=[], manual_preferences=[], has_submitted=False),
        ]

        StudentProposal.objects.bulk_create(students)
        self.stdout.write(self.style.SUCCESS(f'Created {len(students)} Students.'))