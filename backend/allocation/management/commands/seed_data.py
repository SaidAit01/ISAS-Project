from django.core.management.base import BaseCommand
from allocation.models import StudentProposal, SupervisorProfile

class Command(BaseCommand):
    help = 'Seeds the database with a large, varied batch of students and supervisors'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Wiping old data...'))
        StudentProposal.objects.all().delete()
        SupervisorProfile.objects.all().delete()

        # --- BATCH 1: 10 SUPERVISORS ---
        supervisors = [
            SupervisorProfile(name="Dr. Turing", research_interests="Artificial Intelligence, Machine Learning, Deep Learning, Natural Language Processing", capacity=5),
            SupervisorProfile(name="Dr. Lovelace", research_interests="Web Development, React, User Experience, Front-End Architecture, Accessibility", capacity=4),
            SupervisorProfile(name="Dr. Hopper", research_interests="Software Engineering, Compilers, Legacy Systems, Java, System Architecture", capacity=4),
            SupervisorProfile(name="Dr. Dijkstra", research_interests="Algorithms, Graph Theory, Network Routing, Theoretical Computer Science", capacity=3),
            SupervisorProfile(name="Dr. Berners-Lee", research_interests="Semantic Web, API Design, Distributed Systems, Web Security", capacity=5),
            SupervisorProfile(name="Dr. Neumann", research_interests="Computer Architecture, Embedded Systems, IoT, Hardware Design, C++", capacity=4),
            SupervisorProfile(name="Dr. Shannon", research_interests="Information Theory, Cryptography, Data Compression, Cyber Security, Blockchain", capacity=5),
            SupervisorProfile(name="Dr. McCarthy", research_interests="Functional Programming, LISP, Symbolic AI, Logic Programming", capacity=2),
            SupervisorProfile(name="Dr. Knuth", research_interests="Algorithm Analysis, Data Structures, Typography, Mathematical Computing", capacity=3),
            SupervisorProfile(name="Dr. Hamilton", research_interests="Mission Critical Systems, Software Reliability, Aerospace Computing, Testing", capacity=4),
                        SupervisorProfile(name="Dr. Simon Patel", research_interests="Data Science, Big Data, Predictive Modelling, Hadoop, Apache Spark", capacity=3),
            SupervisorProfile(name="Prof. Laura Jenkins", research_interests="Robotics, Autonomous Systems, Cybernetics, Computer Vision, ROS", capacity=4),
            SupervisorProfile(name="Dr. Arthur Pendelton", research_interests="Computational Biology, Bioinformatics, Genomics, Python", capacity=2),
            SupervisorProfile(name="Dr. Chloe Davies", research_interests="Cognitive Computing, Human-Computer Interaction, Accessibility, UI Design", capacity=3),
            SupervisorProfile(name="Prof. Michael O'Connor", research_interests="Cloud Architecture, Distributed Storage, AWS, Serverless Computing", capacity=5),
            SupervisorProfile(name="Dr. Fatima Rahman", research_interests="Ethics in AI, Algorithmic Bias, Tech Policy, Responsible Computing", capacity=2),
            SupervisorProfile(name="Dr. David Chang", research_interests="Augmented Reality, Virtual Reality, Unity3D, 3D Rendering", capacity=3),
            SupervisorProfile(name="Prof. Elizabeth Sterling", research_interests="Audio Processing, Speech Recognition, Digital Signal Processing", capacity=4),
            SupervisorProfile(name="Dr. George Clarke", research_interests="Educational Technology, Gamification, E-Learning Platforms", capacity=3),
            SupervisorProfile(name="Dr. Hannah Wright", research_interests="Digital Forensics, Incident Response, Cyber Security, Malware Analysis", capacity=4),
            SupervisorProfile(name="Prof. Ian Mitchell", research_interests="High-Frequency Trading, Low-Latency Networks, FinTech, C++", capacity=2),
            SupervisorProfile(name="Dr. Jessica Taylor", research_interests="Aerospace Computing, Telemetry, Unmanned Aerial Vehicles, Embedded C", capacity=3),
            SupervisorProfile(name="Dr. Kevin Ndlovu", research_interests="Blockchain Governance, Smart Contracts, Distributed Ledgers, Ethereum", capacity=4),
            SupervisorProfile(name="Prof. Liam Smith", research_interests="Psycholinguistics, Sentiment Analysis, Advanced NLP, Transformers", capacity=3),
            SupervisorProfile(name="Dr. Maria Gonzalez", research_interests="Medical Image Processing, CNNs, Health Informatics, PyTorch", capacity=4),
            SupervisorProfile(name="Dr. Nathan Brooks", research_interests="Agile Methodologies, Software Project Management, DevOps, CI/CD", capacity=5),
            SupervisorProfile(name="Prof. Olivia Green", research_interests="Anomaly Detection, Intrusion Detection Systems, Network Defence", capacity=3),
            SupervisorProfile(name="Dr. Peter Robinson", research_interests="Epidemiological Modelling, Python, Data Visualization, Statistics", capacity=2),
            SupervisorProfile(name="Dr. Rachel Adams", research_interests="Unconventional Computing, Quantum Cryptography, Theoretical Physics", capacity=2),
            SupervisorProfile(name="Prof. Samuel Harris", research_interests="Chemistry Informatics, Simulation, High Performance Computing", capacity=3),
            SupervisorProfile(name="Dr. Thomas Hughes", research_interests="Mobile App Development, React Native, Swift, iOS Architecture", capacity=4),
            SupervisorProfile(name="Dr. Uma Chatterjee", research_interests="Legal Tech, Automated Compliance, Logic Programming, Expert Systems", capacity=3),
            SupervisorProfile(name="Prof. Victor Evans", research_interests="Supply Chain Logistics, Optimization Algorithms, Operations Research", capacity=4),
            SupervisorProfile(name="Dr. William Baker", research_interests="Physical Security Systems, Access Control, IoT, Hardware Hacking", capacity=3),
            SupervisorProfile(name="Dr. Zara Ali", research_interests="Graph Databases, Neo4j, Data Structures, NoSQL", capacity=4),
        ]
        SupervisorProfile.objects.bulk_create(supervisors)
        self.stdout.write(self.style.SUCCESS(f'Created {len(supervisors)} Supervisors.'))

        # --- BATCH 1: 15 STUDENTS (VARIED LENGTHS) ---
        students = [
 # --- LONG PROPOSALS (~150 - 180 words) ---
            StudentProposal(
                name="Eleanor Davies",
                topic_description="The rapid advancement of artificial intelligence has opened new avenues for medical diagnostics. In this project, I propose to develop a highly robust Convolutional Neural Network (CNN) specifically tailored for the early detection of diabetic retinopathy from retinal fundus images. Currently, manual diagnosis by ophthalmologists is time-consuming and prone to human error. By leveraging deep learning frameworks such as PyTorch and TensorFlow, I intend to train a model on a publicly available dataset of 35,000 images. The methodology will involve extensive data preprocessing, including data augmentation and contrast enhancement, followed by transfer learning using pre-trained architectures like ResNet50 or EfficientNet. I will evaluate the model's efficacy using precision, recall, and the F1-score, aiming for an accuracy exceeding 92%. Furthermore, I plan to develop a rudimentary web interface using React to allow medical professionals to upload images and receive instantaneous diagnostic predictions. This project sits at the intersection of machine learning and healthcare, demanding rigorous testing to ensure clinical reliability and software safety.",
                manual_preferences=["Dr. Turing", "Dr. Lovelace"]
            ),
            StudentProposal(
                name="Marcus Johnson",
                topic_description="With the exponential growth of Internet of Things (IoT) devices within smart home environments, the attack surface for malicious actors has widened significantly. This dissertation aims to critically analyse the vulnerabilities inherent in standard household IoT networks. I will construct a simulated smart home environment using virtual machines and physical Raspberry Pi devices to act as smart nodes. Using penetration testing tools such as Wireshark, Metasploit, and Nmap, I will systematically attempt to exploit known vulnerabilities in the Zigbee and standard Wi-Fi protocols. Following the vulnerability assessment, the core of this project will involve designing and implementing a lightweight intrusion detection system (IDS) using Python. This IDS will monitor network traffic in real-time, utilising statistical analysis to detect anomalous behaviour indicative of a distributed denial-of-service (DDoS) attack or unauthorised data exfiltration. The final deliverable will be a comprehensive security report alongside the functional IDS software, contributing to the broader field of cryptography and network defence.",
                manual_preferences=["Dr. Shannon", "Dr. Berners-Lee"]
            ),
            StudentProposal(
                name="Sophia Chen",
                topic_description="Modern software engineering practices heavily rely on continuous integration and continuous deployment (CI/CD) pipelines to maintain code quality. However, legacy systems written in older languages often struggle to integrate into these modern agile workflows. My project proposes to build an automated refactoring tool that bridges this gap. The tool will parse legacy Java codebases, identify anti-patterns, and automatically suggest or implement structural improvements without altering the system's external behaviour. I will employ abstract syntax tree (AST) manipulation to safely refactor the code. The evaluation will involve testing the tool against several open-source legacy projects, measuring the reduction in technical debt using static analysis metrics such as cyclomatic complexity and code churn. This research will require a deep understanding of compiler design, system architecture, and software reliability principles, aiming to provide a practical tool for enterprise software maintenance.",
                manual_preferences=["Dr. Hopper", "Dr. Hamilton", "Dr. Knuth"]
            ),
            StudentProposal(
                name="Benjamin Clarke",
                topic_description="While contemporary artificial intelligence relies heavily on statistical machine learning, there remains significant untapped potential in classical symbolic AI and logic programming for domains requiring strict deterministic outcomes, such as automated legal compliance. I propose to develop a highly structured rule-based expert system utilising LISP to parse and evaluate complex smart contracts. By translating natural language contractual clauses into formal mathematical logic, the system will verify whether specific conditions breach regulatory compliance standards. This will involve designing a novel inference engine capable of backward and forward chaining. The evaluation will benchmark the system's reasoning accuracy against a dataset of 500 historically adjudicated contract disputes. This project merges functional programming with theoretical computer science to provide a highly reliable, explainable AI alternative to 'black box' neural networks.",
                manual_preferences=["Dr. McCarthy", "Dr. Turing"]
            ),
            StudentProposal(
                name="Charlotte Lewis",
                topic_description="The foundation of any future smart city relies on the seamless integration of embedded systems capable of real-time data processing under strict power constraints. This dissertation focuses on hardware design for urban traffic monitoring. I will engineer a custom sensor node utilising a low-power microcontroller programmed entirely in bare-metal C++. The node will interface with piezoelectric sensors to detect vehicle weight and velocity, transmitting this data via a secure, low-latency API design to a central distributed system. A critical component of this research will be optimising the C++ firmware to minimise CPU cycles and memory footprint, extending the battery life of the IoT device to a minimum of two years. Furthermore, the data transmission layer must be fortified against interception using lightweight cryptography, bridging the gap between computer architecture and cyber security.",
                manual_preferences=["Dr. Neumann", "Dr. Berners-Lee"]
            ),
            StudentProposal(
                name="William Carter",
                topic_description="Quantum computing represents a paradigm shift in algorithm design. My dissertation will explore the theoretical limits of Shor's algorithm compared to classical cryptographic factoring methods. I will mathematically model the qubit decay rates required to crack modern RSA encryption using simulated quantum environments. This theoretical computer science project will require a deep dive into mathematical computing and cryptography to evaluate the future security of distributed systems.",
                manual_preferences=["Dr. Dijkstra", "Dr. Shannon"]
            ),

            # --- MEDIUM PROPOSALS (~75 - 100 words) ---
            StudentProposal(
                name="Liam O'Connor",
                topic_description="I want to build a fully responsive, accessibility-first e-commerce platform. Most modern web applications fail to adhere to WCAG standards, alienating users with disabilities. Using React for the front-end architecture and Node.js for the API design, I will create a seamless shopping experience. The project will heavily focus on User Experience (UX) and semantic HTML. I will also integrate a secure payment gateway and ensure the database architecture can handle high concurrent traffic.",
                manual_preferences=["Dr. Lovelace"]
            ),
            StudentProposal(
                name="Aisha Rahman",
                topic_description="My project focuses on Embedded Systems and IoT. I intend to design a smart agricultural monitoring system using C++ and microcontrollers. The hardware will collect soil moisture and temperature data, transmitting it securely to a cloud server. The challenge lies in optimizing the C++ code for extremely low power consumption so the hardware can run on solar energy indefinitely. It requires a strong grasp of computer architecture and hardware design.",
                manual_preferences=["Dr. Neumann"]
            ),
            StudentProposal(
                name="Noah Smith",
                topic_description="This project will explore advanced network routing algorithms. I plan to simulate large-scale graph networks and compare the efficiency of Dijkstra's algorithm against A* and Bellman-Ford under heavily congested network conditions. The output will be a visual dashboard written in Python that allows users to alter network weights in real-time and observe how the different theoretical computer science algorithms adapt to find the optimal path.",
                manual_preferences=["Dr. Dijkstra", "Dr. Knuth"]
            ),
            StudentProposal(
                name="Isabella Rossi",
                topic_description="I am fascinated by symbolic AI and logic programming. Instead of using modern neural networks, I want to build a classical expert system using LISP. The system will be designed to parse complex legal documents and logically deduce whether certain contractual obligations have been met based on a predefined set of rules. This is an exploration into functional programming and rule-based artificial intelligence.",
                manual_preferences=["Dr. McCarthy"]
            ),
            StudentProposal(
                name="James Sterling",
                topic_description="I aim to develop a secure, decentralized messaging application utilizing blockchain technology. The core focus will be on implementing end-to-end encryption and exploring advanced cryptography techniques to ensure data integrity and user privacy. I will investigate how information theory principles apply to data compression within the blockchain ledger to improve message transmission speeds without compromising cyber security.",
                manual_preferences=["Dr. Shannon"]
            ),
            StudentProposal(
                name="Samuel Walker",
                topic_description="Software reliability is paramount in mission critical systems. I intend to build a robust testing framework designed specifically for aerospace computing modules. Using Java and automated unit testing methodologies, the framework will simulate extreme hardware failure states to observe how the software architecture gracefully degrades. The goal is to ensure zero unhandled exceptions during runtime, proving the system's reliability.",
                manual_preferences=["Dr. Hamilton", "Dr. Hopper"]
            ),
            StudentProposal(
                name="Grace Hall",
                topic_description="I want to analyse the performance of highly complex data structures when rendering typography for the web. By building a custom rendering engine, I will benchmark the mathematical computing efficiency of B-Trees versus Red-Black trees when parsing thousands of font ligatures. This project marries algorithm analysis with front-end visual performance.",
                manual_preferences=["Dr. Knuth"]
            ),
            StudentProposal(
                name="Alexander Young",
                topic_description="Distributed systems are highly vulnerable to API abuse. My project will construct a secure Semantic Web application that strictly enforces data access policies. I will implement OAuth 2.0 alongside novel web security protocols to ensure that inter-service communication remains tamper-proof, focusing heavily on secure API design.",
                manual_preferences=["Dr. Berners-Lee", "Dr. Shannon"]
            ),
            StudentProposal(
                name="Daniel Baker",
                topic_description="I am focusing on Human-Computer Interaction and accessibility. I want to evaluate how elderly users interact with modern mobile interfaces, using React Native to build a prototype app that adapts its UI based on the user's motor skills. User Experience is the core of this project.",
                manual_preferences=["Dr. Lovelace"]
            ),
            StudentProposal(
                name="Emily Nelson",
                topic_description="My project will evaluate the efficiency of Docker containers versus traditional virtual machines in a cloud computing environment using AWS. I will deploy a distributed system architecture and measure the latency, resource usage, and boot times under heavy load to determine the best approach for modern web scalability.",
                manual_preferences=["Dr. Berners-Lee", "Dr. Hopper"]
            ),

            # --- SHORT / LAZY PROPOSALS (< 40 words) ---
            StudentProposal(
                name="Chloe Patel",
                topic_description="I want to do a project on Natural Language Processing. Maybe a chatbot that can talk to students about their university schedule using machine learning.",
                manual_preferences=[]
            ),
            StudentProposal(
                name="Oliver Brown",
                topic_description="Building a portfolio website using React and some API design. Needs to look good.",
                manual_preferences=["Dr. Lovelace"]
            ),
            StudentProposal(
                name="Mia Taylor",
                topic_description="Programming a drone using C++ and embedded systems.",
                manual_preferences=[]
            ),
            StudentProposal(
                name="Lucas Anderson",
                topic_description="Comparing data structures and algorithm analysis for sorting large datasets.",
                manual_preferences=["Dr. Knuth", "Dr. Dijkstra"]
            ),
            StudentProposal(
                name="Harper White",
                topic_description="Ethical hacking project looking at web security and finding bugs in legacy systems.",
                manual_preferences=[]
            ),
            StudentProposal(
                name="Ethan Harris",
                topic_description="Testing software reliability for aerospace computing. Making sure code doesn't crash.",
                manual_preferences=["Dr. Hamilton"]
            ),
            StudentProposal(
                name="Amelia Martin",
                topic_description="A Java app for system architecture.",
                manual_preferences=[]
            ),
            StudentProposal(
                name="Lily King",
                topic_description="Doing some theoretical computer science about network routing and graph theory.",
                manual_preferences=["Dr. Dijkstra"]
            ),
            StudentProposal(
                name="Henry Wright",
                topic_description="IoT hardware in C++.",
                manual_preferences=[]
            ),
            StudentProposal(
                name="Zoe Scott",
                topic_description="Compilers and software engineering.",
                manual_preferences=["Dr. Hopper"]
            ),
            StudentProposal(
                name="Jack Green",
                topic_description="I like maths and maybe some web stuff or security. Something with algorithms?",
                manual_preferences=[]
            ),
            StudentProposal(
                name="Victoria Adams",
                topic_description="Deep learning model for image recognition.",
                manual_preferences=["Dr. Turing"]
            ),
            StudentProposal(
                name="Sophie Mitchell",
                topic_description="Developing a smart contract on Ethereum.",
                manual_preferences=["Dr. Shannon"]
            ),
            StudentProposal(
                name="Thomas Roberts",
                topic_description="A database project.",
                manual_preferences=[]
            ),
            # --- BATCH 3: 15 ADDITIONAL STUDENTS (VARIED LENGTHS) ---
            StudentProposal(
                name="Alice Thompson",
                topic_description="As artificial intelligence systems become increasingly integrated into critical infrastructure, the necessity for algorithmic transparency and ethical decision-making frameworks is paramount. My research will focus on developing a novel auditing tool for deep learning models to identify and mitigate inherent biases in training datasets. I plan to use Natural Language Processing to analyse model outputs and generate human-readable explanations of the AI's logic, bridging the gap between complex neural networks and regulatory compliance requirements.",
                manual_preferences=["Dr. Turing", "Dr. McCarthy"]
            ),
            StudentProposal(
                name="David White",
                topic_description="The rapid sequencing of genomic data presents a monumental challenge for computational biology. I propose to investigate and optimise string-matching algorithms specifically tailored for massive DNA datasets. By comparing the time and space complexity of the Boyer-Moore algorithm against suffix trees and modern hash-based approaches, I aim to significantly reduce the computational overhead required for genetic sequence alignment. This theoretical computer science project relies heavily on advanced mathematical computing.",
                manual_preferences=["Dr. Knuth", "Dr. Dijkstra"]
            ),
            StudentProposal(
                name="Maya Patel",
                topic_description="Enterprise migration to multi-cloud architectures has introduced unprecedented vulnerabilities regarding data provenance and access control. This project will engineer a distributed logging system utilising cryptographic hashes and blockchain principles to ensure that cross-server API communications cannot be tampered with. I will be evaluating the system against standard web security benchmarks to prove its resilience against man-in-the-middle attacks.",
                manual_preferences=["Dr. Berners-Lee", "Dr. Shannon"]
            ),
            StudentProposal(
                name="Luke Robinson",
                topic_description="I wish to explore real-time physics rendering in video game engines using C++. The focus will be on optimising collision detection algorithms for multi-threaded hardware architectures, aiming to squeeze maximum performance out of embedded and constrained systems.",
                manual_preferences=["Dr. Neumann", "Dr. Dijkstra"]
            ),
            StudentProposal(
                name="Ruby Evans",
                topic_description="Developing a cross-platform mobile application for mental health tracking. The core of the research is User Experience (UX) design, ensuring the interface is highly accessible and calming for users experiencing anxiety. I will build the front-end architecture using React Native.",
                manual_preferences=["Dr. Lovelace"]
            ),
            StudentProposal(
                name="Leo Wood",
                topic_description="Investigating optimisation passes in modern compilers for functional programming languages. I want to build a small LISP interpreter in Java that compiles down to highly efficient bytecode, focusing heavily on software engineering and system architecture principles.",
                manual_preferences=["Dr. Hopper", "Dr. McCarthy"]
            ),
            StudentProposal(
                name="Chloe Hughes",
                topic_description="Building a robust flight controller for autonomous UAVs using embedded C. The project requires strict adherence to software reliability standards to ensure the mission critical systems do not fail mid-flight.",
                manual_preferences=["Dr. Hamilton", "Dr. Neumann"]
            ),
            StudentProposal(
                name="Arthur King",
                topic_description="Analysing financial market sentiment using Natural Language Processing on large streams of Twitter data. I will use deep learning models to classify the tweets and predict minor market fluctuations.",
                manual_preferences=["Dr. Turing"]
            ),
            StudentProposal(
                name="Freya Harrison",
                topic_description="A website for a local bakery using React and good UX.",
                manual_preferences=["Dr. Lovelace"]
            ),
            StudentProposal(
                name="Mason Fox",
                topic_description="Machine learning and artificial intelligence for predicting football scores.",
                manual_preferences=["Dr. Turing"]
            ),
            StudentProposal(
                name="Isla Davies",
                topic_description="Researching cryptography and secure blockchain ledgers.",
                manual_preferences=["Dr. Shannon"]
            ),
            StudentProposal(
                name="Jacob Morgan",
                topic_description="Creating automated software testing tools in Java.",
                manual_preferences=["Dr. Hopper", "Dr. Hamilton"]
            ),
            StudentProposal(
                name="Mia Griffiths",
                topic_description="Algorithms for fast graph traversal and network routing.",
                manual_preferences=["Dr. Dijkstra"]
            ),
            StudentProposal(
                name="Harry Kelly",
                topic_description="Cyber security penetration testing on distributed web apps.",
                manual_preferences=["Dr. Berners-Lee"]
            ),
            StudentProposal(
                name="Grace Price",
                topic_description="An IoT smart thermostat using C++ and hardware design.",
                manual_preferences=["Dr. Neumann"]
            ),
            # --- BATCH 4: 15 ADDITIONAL STUDENTS (BRINGING TOTAL TO 60) ---
            StudentProposal(
                name="Elijah Ward",
                topic_description="The intersection of quantum computing and machine learning offers unprecedented capabilities for pattern recognition. This dissertation will investigate the implementation of Quantum Support Vector Machines (QSVM) using Qiskit. I aim to mathematically demonstrate how quantum entanglement can process high-dimensional datasets exponentially faster than classical AI algorithms. This highly theoretical project will require rigorous algorithm analysis and an advanced understanding of linear algebra and quantum states.",
                manual_preferences=["Dr. Dijkstra", "Dr. Turing"]
            ),
            StudentProposal(
                name="Zara Khan",
                topic_description="Medical devices such as pacemakers are increasingly reliant on embedded IoT technology, creating severe vulnerabilities. My project proposes a novel hardware design utilizing C++ to implement an air-gapped security protocol for biometric monitoring systems. By separating the data transmission layer from the core life-support firmware, I will ensure that even if the network is compromised by cyber security threats, the hardware architecture remains resilient. This is a mission-critical systems engineering task.",
                manual_preferences=["Dr. Neumann", "Dr. Shannon"]
            ),
            StudentProposal(
                name="Mohammed Ali",
                topic_description="I propose to build an automated grading system for university programming assignments. Leveraging Natural Language Processing and Abstract Syntax Tree (AST) parsing, the software will not only check if the Java code compiles, but will semantically analyse the code quality, identifying poor software engineering practices and suggesting architectural improvements.",
                manual_preferences=["Dr. Hopper", "Dr. Turing"]
            ),
            StudentProposal(
                name="Lucy Campbell",
                topic_description="Most graph databases struggle with highly volatile, rapidly changing data structures. I want to build a theoretical benchmarking suite in C++ to compare the latency of Neo4j against a custom-built distributed hash table when routing millions of concurrent network requests. This will focus heavily on algorithm analysis and data structures.",
                manual_preferences=["Dr. Knuth", "Dr. Dijkstra"]
            ),
            StudentProposal(
                name="Harrison Bell",
                topic_description="A front-end development project focusing entirely on Web Accessibility for visually impaired users. I will use React to build a dynamic screen-reader interface that interprets spatial UI layouts into semantic audio cues, aiming to vastly improve modern User Experience.",
                manual_preferences=["Dr. Lovelace"]
            ),
            StudentProposal(
                name="Eleanor Murphy",
                topic_description="Swarm robotics requires incredibly efficient network routing algorithms to prevent collisions in mid-air. I will develop a Python simulation to test how drones can use local mesh networks to share telemetry data without relying on a central distributed system.",
                manual_preferences=["Dr. Dijkstra", "Dr. Hamilton"]
            ),
            StudentProposal(
                name="Jackson Stewart",
                topic_description="An investigation into modern legacy systems within the UK banking sector. I want to map out how COBOL databases can be safely encapsulated and interacted with using modern Semantic Web APIs without causing catastrophic software failure.",
                manual_preferences=["Dr. Hopper", "Dr. Berners-Lee"]
            ),
            StudentProposal(
                name="Sebastian Cook",
                topic_description="I want to design an electronic voting system using blockchain. It will use cryptography to keep votes anonymous while ensuring the ledger is public and mathematically verifiable, protecting democratic integrity.",
                manual_preferences=["Dr. Shannon", "Dr. Berners-Lee"]
            ),
            StudentProposal(
                name="Aria Bailey",
                topic_description="Building a 2D platformer game in Java, focusing on software architecture and object-oriented design patterns.",
                manual_preferences=["Dr. Hopper"]
            ),
            StudentProposal(
                name="Logan Parker",
                topic_description="Using deep learning to classify different types of clouds in satellite imagery. An AI and computer vision project.",
                manual_preferences=["Dr. Turing"]
            ),
            StudentProposal(
                name="Evelyn Collins",
                topic_description="I want to test the software reliability of an open-source flight simulator.",
                manual_preferences=["Dr. Hamilton"]
            ),
            StudentProposal(
                name="Ryan Sanchez",
                topic_description="A web app for tracking gym workouts using React.",
                manual_preferences=["Dr. Lovelace"]
            ),
            StudentProposal(
                name="Sofia Morris",
                topic_description="Cyber security analysis of default router passwords.",
                manual_preferences=["Dr. Shannon"]
            ),
            StudentProposal(
                name="Nathan Rogers",
                topic_description="Maths and algorithms project.",
                manual_preferences=[]
            ),
            StudentProposal(
                name="Harper Reed",
                topic_description="IoT sensors for tracking my cat using C++.",
                manual_preferences=["Dr. Neumann"]
            ),
                        # --- BATCH 3: 15 ADDITIONAL STUDENTS (VARIED LENGTHS) ---
            StudentProposal(
                name="Alice Thompson",
                topic_description="As artificial intelligence systems become increasingly integrated into critical infrastructure, the necessity for algorithmic transparency and ethical decision-making frameworks is paramount. My research will focus on developing a novel auditing tool for deep learning models to identify and mitigate inherent biases in training datasets. I plan to use Natural Language Processing to analyse model outputs and generate human-readable explanations of the AI's logic, bridging the gap between complex neural networks and regulatory compliance requirements.",
                manual_preferences=["Dr. Turing", "Dr. McCarthy"]
            ),
            StudentProposal(
                name="David White",
                topic_description="The rapid sequencing of genomic data presents a monumental challenge for computational biology. I propose to investigate and optimise string-matching algorithms specifically tailored for massive DNA datasets. By comparing the time and space complexity of the Boyer-Moore algorithm against suffix trees and modern hash-based approaches, I aim to significantly reduce the computational overhead required for genetic sequence alignment. This theoretical computer science project relies heavily on advanced mathematical computing.",
                manual_preferences=["Dr. Knuth", "Dr. Dijkstra"]
            ),
            StudentProposal(
                name="Maya Patel",
                topic_description="Enterprise migration to multi-cloud architectures has introduced unprecedented vulnerabilities regarding data provenance and access control. This project will engineer a distributed logging system utilising cryptographic hashes and blockchain principles to ensure that cross-server API communications cannot be tampered with. I will be evaluating the system against standard web security benchmarks to prove its resilience against man-in-the-middle attacks.",
                manual_preferences=["Dr. Berners-Lee", "Dr. Shannon"]
            ),
            StudentProposal(
                name="Luke Robinson",
                topic_description="I wish to explore real-time physics rendering in video game engines using C++. The focus will be on optimising collision detection algorithms for multi-threaded hardware architectures, aiming to squeeze maximum performance out of embedded and constrained systems.",
                manual_preferences=["Dr. Neumann", "Dr. Dijkstra"]
            ),
            StudentProposal(
                name="Ruby Evans",
                topic_description="Developing a cross-platform mobile application for mental health tracking. The core of the research is User Experience (UX) design, ensuring the interface is highly accessible and calming for users experiencing anxiety. I will build the front-end architecture using React Native.",
                manual_preferences=["Dr. Lovelace"]
            ),
            StudentProposal(
                name="Leo Wood",
                topic_description="Investigating optimisation passes in modern compilers for functional programming languages. I want to build a small LISP interpreter in Java that compiles down to highly efficient bytecode, focusing heavily on software engineering and system architecture principles.",
                manual_preferences=["Dr. Hopper", "Dr. McCarthy"]
            ),
            StudentProposal(
                name="Chloe Hughes",
                topic_description="Building a robust flight controller for autonomous UAVs using embedded C. The project requires strict adherence to software reliability standards to ensure the mission critical systems do not fail mid-flight.",
                manual_preferences=["Dr. Hamilton", "Dr. Neumann"]
            ),
            StudentProposal(
                name="Arthur King",
                topic_description="Analysing financial market sentiment using Natural Language Processing on large streams of Twitter data. I will use deep learning models to classify the tweets and predict minor market fluctuations.",
                manual_preferences=["Dr. Turing"]
            ),
            StudentProposal(
                name="Freya Harrison",
                topic_description="A website for a local bakery using React and good UX.",
                manual_preferences=["Dr. Lovelace"]
            ),
            StudentProposal(
                name="Mason Fox",
                topic_description="Machine learning and artificial intelligence for predicting football scores.",
                manual_preferences=["Dr. Turing"]
            ),
            StudentProposal(
                name="Isla Davies",
                topic_description="Researching cryptography and secure blockchain ledgers.",
                manual_preferences=["Dr. Shannon"]
            ),
            StudentProposal(
                name="Jacob Morgan",
                topic_description="Creating automated software testing tools in Java.",
                manual_preferences=["Dr. Hopper", "Dr. Hamilton"]
            ),
            StudentProposal(
                name="Mia Griffiths",
                topic_description="Algorithms for fast graph traversal and network routing.",
                manual_preferences=["Dr. Dijkstra"]
            ),
            StudentProposal(
                name="Harry Kelly",
                topic_description="Cyber security penetration testing on distributed web apps.",
                manual_preferences=["Dr. Berners-Lee"]
            ),
            StudentProposal(
                name="Grace Price",
                topic_description="An IoT smart thermostat using C++ and hardware design.",
                manual_preferences=["Dr. Neumann"]
            ),
            # --- BATCH 4: 15 ADDITIONAL STUDENTS (BRINGING TOTAL TO 60) ---
            StudentProposal(
                name="Elijah Ward",
                topic_description="The intersection of quantum computing and machine learning offers unprecedented capabilities for pattern recognition. This dissertation will investigate the implementation of Quantum Support Vector Machines (QSVM) using Qiskit. I aim to mathematically demonstrate how quantum entanglement can process high-dimensional datasets exponentially faster than classical AI algorithms. This highly theoretical project will require rigorous algorithm analysis and an advanced understanding of linear algebra and quantum states.",
                manual_preferences=["Dr. Dijkstra", "Dr. Turing"]
            ),
            StudentProposal(
                name="Zara Khan",
                topic_description="Medical devices such as pacemakers are increasingly reliant on embedded IoT technology, creating severe vulnerabilities. My project proposes a novel hardware design utilizing C++ to implement an air-gapped security protocol for biometric monitoring systems. By separating the data transmission layer from the core life-support firmware, I will ensure that even if the network is compromised by cyber security threats, the hardware architecture remains resilient. This is a mission-critical systems engineering task.",
                manual_preferences=["Dr. Neumann", "Dr. Shannon"]
            ),
            StudentProposal(
                name="Mohammed Ali",
                topic_description="I propose to build an automated grading system for university programming assignments. Leveraging Natural Language Processing and Abstract Syntax Tree (AST) parsing, the software will not only check if the Java code compiles, but will semantically analyse the code quality, identifying poor software engineering practices and suggesting architectural improvements.",
                manual_preferences=["Dr. Hopper", "Dr. Turing"]
            ),
            StudentProposal(
                name="Lucy Campbell",
                topic_description="Most graph databases struggle with highly volatile, rapidly changing data structures. I want to build a theoretical benchmarking suite in C++ to compare the latency of Neo4j against a custom-built distributed hash table when routing millions of concurrent network requests. This will focus heavily on algorithm analysis and data structures.",
                manual_preferences=["Dr. Knuth", "Dr. Dijkstra"]
            ),
            StudentProposal(
                name="Harrison Bell",
                topic_description="A front-end development project focusing entirely on Web Accessibility for visually impaired users. I will use React to build a dynamic screen-reader interface that interprets spatial UI layouts into semantic audio cues, aiming to vastly improve modern User Experience.",
                manual_preferences=["Dr. Lovelace"]
            ),
            StudentProposal(
                name="Eleanor Murphy",
                topic_description="Swarm robotics requires incredibly efficient network routing algorithms to prevent collisions in mid-air. I will develop a Python simulation to test how drones can use local mesh networks to share telemetry data without relying on a central distributed system.",
                manual_preferences=["Dr. Dijkstra", "Dr. Hamilton"]
            ),
            StudentProposal(
                name="Jackson Stewart",
                topic_description="An investigation into modern legacy systems within the UK banking sector. I want to map out how COBOL databases can be safely encapsulated and interacted with using modern Semantic Web APIs without causing catastrophic software failure.",
                manual_preferences=["Dr. Hopper", "Dr. Berners-Lee"]
            ),
            StudentProposal(
                name="Sebastian Cook",
                topic_description="I want to design an electronic voting system using blockchain. It will use cryptography to keep votes anonymous while ensuring the ledger is public and mathematically verifiable, protecting democratic integrity.",
                manual_preferences=["Dr. Shannon", "Dr. Berners-Lee"]
            ),
            StudentProposal(
                name="Aria Bailey",
                topic_description="Building a 2D platformer game in Java, focusing on software architecture and object-oriented design patterns.",
                manual_preferences=["Dr. Hopper"]
            ),
            StudentProposal(
                name="Logan Parker",
                topic_description="Using deep learning to classify different types of clouds in satellite imagery. An AI and computer vision project.",
                manual_preferences=["Dr. Turing"]
            ),
            StudentProposal(
                name="Evelyn Collins",
                topic_description="I want to test the software reliability of an open-source flight simulator.",
                manual_preferences=["Dr. Hamilton"]
            ),
            StudentProposal(
                name="Ryan Sanchez",
                topic_description="A web app for tracking gym workouts using React.",
                manual_preferences=["Dr. Lovelace"]
            ),
            StudentProposal(
                name="Sofia Morris",
                topic_description="Cyber security analysis of default router passwords.",
                manual_preferences=["Dr. Shannon"]
            ),
            StudentProposal(
                name="Nathan Rogers",
                topic_description="Maths and algorithms project.",
                manual_preferences=[]
            ),
            StudentProposal(
                name="Harper Reed",
                topic_description="IoT sensors for tracking my cat using C++.",
                manual_preferences=["Dr. Neumann"]
            ),
            # --- BATCH 5: 40 FINAL STUDENTS (BRINGING TOTAL TO 100) ---
            
            # --- The High Achievers (Long Proposals) ---
            StudentProposal(
                name="Oliver Smith",
                topic_description="Brain-Computer Interfaces (BCI) offer life-changing potential for users with severe motor disabilities. This project aims to translate raw electroencephalogram (EEG) signals into actionable keyboard commands using a highly optimised Recurrent Neural Network (RNN). I will utilize PyTorch to train the model on the publicly available PhysioNet dataset. The challenge lies in filtering the immense noise inherent in non-invasive EEG hardware. I aim to achieve a signal-to-noise ratio that allows for real-time, basic text input, thereby bridging the gap between hardware design, signal processing, and advanced machine learning.",
                manual_preferences=["Dr. Turing", "Dr. Neumann"]
            ),
            StudentProposal(
                name="Emma Johnson",
                topic_description="Microservice architectures have largely replaced monolithic systems in enterprise software engineering. However, the overhead of orchestrating hundreds of containerised services often introduces severe latency. I propose to build a theoretical benchmarking tool in Go and Java to evaluate the network routing efficiency of Kubernetes against a novel, lightweight service mesh of my own design. I will focus heavily on system architecture, API design, and distributed systems theory to prove whether current industry standards are mathematically optimal.",
                manual_preferences=["Dr. Berners-Lee", "Dr. Hopper"]
            ),
            StudentProposal(
                name="Noah Williams",
                topic_description="The proliferation of deepfakes poses a critical cyber security threat to democratic institutions. I intend to develop a forensic tool using Natural Language Processing and Computer Vision to detect algorithmic anomalies in video artifacts. By mathematically analysing the pixel-level compression patterns and audio-visual sync variations, the software will output a probability score regarding the media's authenticity. This involves cryptography, information theory, and deep learning.",
                manual_preferences=["Dr. Shannon", "Dr. Turing"]
            ),
            StudentProposal(
                name="Ava Jones",
                topic_description="Optimising the garbage collector in the Java Virtual Machine (JVM) for high-frequency trading applications. In mission critical systems where a microsecond delay results in massive financial loss, standard software reliability metrics are insufficient. I will mathematically model memory allocation strategies and alter the JVM source code to prioritize deterministic latency over overall throughput.",
                manual_preferences=["Dr. Hopper", "Dr. Hamilton"]
            ),
            
            # --- The Standard Cohort (Medium Proposals) ---
            StudentProposal(
                name="William Brown",
                topic_description="I want to create an educational web application that visually demonstrates how complex algorithms work. Using React, I will build an interactive canvas where students can step through Graph Theory concepts like Dijkstra's and A* pathfinding. The focus will be on excellent User Experience and clean front-end architecture.",
                manual_preferences=["Dr. Lovelace", "Dr. Dijkstra"]
            ),
            StudentProposal(
                name="Sophia Davis",
                topic_description="A peer-to-peer file sharing protocol written in C++. I want to explore theoretical computer science by implementing a custom Distributed Hash Table (DHT) to route network requests without a central server. Security and cryptography will be necessary to prevent malicious node injection.",
                manual_preferences=["Dr. Dijkstra", "Dr. Shannon"]
            ),
            StudentProposal(
                name="James Miller",
                topic_description="Building a symbolic logic calculator. Most calculators do arithmetic, but I want to build a tool using LISP that can simplify complex boolean algebra expressions and mathematically prove logical equivalencies for computer architecture students.",
                manual_preferences=["Dr. McCarthy", "Dr. Knuth"]
            ),
            StudentProposal(
                name="Isabella Wilson",
                topic_description="I am researching the accessibility of modern video games for deaf players. I will build a prototype game engine in Java that translates all crucial audio cues into dynamic visual indicators. Software engineering and UX are the main focus.",
                manual_preferences=["Dr. Lovelace", "Dr. Hopper"]
            ),
            StudentProposal(
                name="Benjamin Moore",
                topic_description="Using machine learning to predict student dropout rates based on virtual learning environment (VLE) login data. A purely data analysis and AI project using Python.",
                manual_preferences=["Dr. Turing"]
            ),
            StudentProposal(
                name="Mia Taylor",
                topic_description="Developing a smart irrigation system. Using an Arduino and C++, the embedded system will read local weather APIs and soil sensors to determine exactly when to water crops, saving water and power.",
                manual_preferences=["Dr. Neumann", "Dr. Berners-Lee"]
            ),
            StudentProposal(
                name="Ewan MacLeod",
                topic_description="Exploring legacy system modernization. I want to build a tool that translates older COBOL data structures into modern JSON formats for Semantic Web APIs. It requires strict software reliability testing.",
                manual_preferences=["Dr. Hopper", "Dr. Hamilton"]
            ),
            StudentProposal(
                name="Lily Anderson",
                topic_description="Mathematical computing project to optimize the rendering of 3D fractals. I will use C++ and focus on algorithm analysis to reduce the time complexity of the render loop.",
                manual_preferences=["Dr. Knuth"]
            ),
            StudentProposal(
                name="Oliver Thomas",
                topic_description="A cyber security project analyzing the vulnerability of contactless payment cards. I will study the NFC protocols and encryption methods used.",
                manual_preferences=["Dr. Shannon"]
            ),
            StudentProposal(
                name="Amelia Jackson",
                topic_description="Building a web-based project management tool like Jira, but simplified for university students. I will use React for the frontend and focus on UI/UX.",
                manual_preferences=["Dr. Lovelace"]
            ),

            # --- The Vague/Lazy Cohort (Short & Extremely Short Proposals) ---
            StudentProposal(name="Lucas White", topic_description="Artificial intelligence for chess.", manual_preferences=["Dr. Turing"]),
            StudentProposal(name="Charlotte Harris", topic_description="A web app for recipes. Using JavaScript and a database.", manual_preferences=["Dr. Lovelace"]),
            StudentProposal(name="Alexander Martin", topic_description="Network routing algorithms and theoretical maths.", manual_preferences=["Dr. Dijkstra"]),
            StudentProposal(name="Harper Thompson", topic_description="Testing code to make sure it is reliable.", manual_preferences=["Dr. Hamilton"]),
            StudentProposal(name="Evelyn Garcia", topic_description="Embedded systems and C++.", manual_preferences=["Dr. Neumann"]),
            StudentProposal(name="Jack Martinez", topic_description="Blockchain security.", manual_preferences=["Dr. Shannon"]),
            StudentProposal(name="Avery Robinson", topic_description="Logic programming in LISP.", manual_preferences=["Dr. McCarthy"]),
            StudentProposal(name="Owen Clark", topic_description="Data structures and maths.", manual_preferences=["Dr. Knuth"]),
            StudentProposal(name="Abigail Rodriguez", topic_description="Software engineering in Java.", manual_preferences=["Dr. Hopper"]),
            StudentProposal(name="Henry Lewis", topic_description="Semantic web API.", manual_preferences=["Dr. Berners-Lee"]),
            StudentProposal(name="Riley Lee", topic_description="Machine learning.", manual_preferences=[]),
            StudentProposal(name="Ella Walker", topic_description="Web development.", manual_preferences=[]),
            StudentProposal(name="Sebastian Hall", topic_description="Algorithms.", manual_preferences=[]),
            StudentProposal(name="Aria Allen", topic_description="Cyber security.", manual_preferences=[]),
            StudentProposal(name="Daniel Young", topic_description="Hardware.", manual_preferences=[]),
            StudentProposal(name="Scarlett Hernandez", topic_description="Maths.", manual_preferences=[]),
            StudentProposal(name="Matthew King", topic_description="Java.", manual_preferences=[]),
            StudentProposal(name="Victoria Wright", topic_description="React.", manual_preferences=[]),
            StudentProposal(name="Joseph Lopez", topic_description="C++.", manual_preferences=[]),
            StudentProposal(name="Chloe Hill", topic_description="AI.", manual_preferences=[]),
            StudentProposal(name="Samuel Scott", topic_description="Testing.", manual_preferences=[]),
            StudentProposal(name="Penelope Green", topic_description="Logic.", manual_preferences=[]),
            StudentProposal(name="David Adams", topic_description="Networks.", manual_preferences=[]),
            StudentProposal(name="Layla Baker", topic_description="Data.", manual_preferences=[]),
            StudentProposal(name="Carter Gonzalez", topic_description="Security.", manual_preferences=[]),
            StudentProposal(name="Zoey Nelson", topic_description="Software.", manual_preferences=[]),
        
        ]

        StudentProposal.objects.bulk_create(students)
        self.stdout.write(self.style.SUCCESS(f'Created {len(students)} Students.'))