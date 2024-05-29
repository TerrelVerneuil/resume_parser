
from fpdf import FPDF
# Define a function to create a resume
def create_resume(role, name, contact, experience, education, skills, certifications):
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", size=24)
    pdf.cell(200, 10, txt=f"{name} - {role}", ln=True, align='C')
    
    # Contact Information
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Contact Information", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Email: {contact['email']}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Phone: {contact['phone']}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Address: {contact['address']}", ln=True, align='L')
    
    # Objective
    pdf.cell(200, 10, txt=f"Objective", ln=True, align='L')
    pdf.multi_cell(0, 10, txt=f"To secure a position as a {role} at a reputable company where I can utilize my skills and experience.")
    
    # Experience
    pdf.cell(200, 10, txt=f"Experience", ln=True, align='L')
    for job in experience:
        pdf.cell(200, 10, txt=f"{job['title']} - {job['company']} ({job['years']})", ln=True, align='L')
        pdf.multi_cell(0, 10, txt=job['description'])
    
    # Education
    pdf.cell(200, 10, txt=f"Education", ln=True, align='L')
    for edu in education:
        pdf.cell(200, 10, txt=f"{edu['degree']} - {edu['institution']} ({edu['years']})", ln=True, align='L')
    
    # Skills
    pdf.cell(200, 10, txt=f"Skills", ln=True, align='L')
    pdf.multi_cell(0, 10, txt=", ".join(skills))
    
    # Certifications
    pdf.cell(200, 10, txt=f"Certifications", ln=True, align='L')
    pdf.multi_cell(0, 10, txt=", ".join(certifications))
    
    return pdf

# Define sample data for each resume
resumes_data = [
    {
        "role": "Software Engineer",
        "name": "John Doe",
        "contact": {"email": "john.doe@example.com", "phone": "123-456-7890", "address": "123 Main St, Anytown, USA"},
        "experience": [
            {"title": "Senior Software Engineer", "company": "Tech Solutions", "years": "2018-Present", "description": "Developed and maintained web applications."},
            {"title": "Software Engineer", "company": "Innovative Apps", "years": "2015-2018", "description": "Worked on backend services and APIs."}
        ],
        "education": [
            {"degree": "BSc in Computer Science", "institution": "State University", "years": "2011-2015"}
        ],
        "skills": ["Python", "Java", "SQL", "AWS"],
        "certifications": ["Certified Java Programmer", "AWS Certified Developer"]
    },
    {
        "role": "Data Scientist",
        "name": "Jane Smith",
        "contact": {"email": "jane.smith@example.com", "phone": "987-654-3210", "address": "456 Market St, Anytown, USA"},
        "experience": [
            {"title": "Lead Data Scientist", "company": "Data Insights", "years": "2019-Present", "description": "Led data analysis projects and developed predictive models."},
            {"title": "Data Analyst", "company": "Analytics Co.", "years": "2016-2019", "description": "Analyzed large datasets to provide business insights."}
        ],
        "education": [
            {"degree": "MSc in Data Science", "institution": "Tech University", "years": "2014-2016"},
            {"degree": "BSc in Statistics", "institution": "State University", "years": "2010-2014"}
        ],
        "skills": ["Python", "R", "SQL", "Machine Learning"],
        "certifications": ["Certified Data Scientist", "Machine Learning Specialist"]
    },
    {
        "role": "Marketing Manager",
        "name": "Michael Johnson",
        "contact": {"email": "michael.johnson@example.com", "phone": "555-123-4567", "address": "789 Elm St, Anytown, USA"},
        "experience": [
            {"title": "Marketing Manager", "company": "Creative Solutions", "years": "2017-Present", "description": "Managed marketing campaigns and social media strategies."},
            {"title": "Marketing Specialist", "company": "Advertise Now", "years": "2014-2017", "description": "Developed content for advertising and promotional materials."}
        ],
        "education": [
            {"degree": "MBA in Marketing", "institution": "Business School", "years": "2012-2014"},
            {"degree": "BA in Communications", "institution": "State University", "years": "2008-2012"}
        ],
        "skills": ["SEO", "Content Marketing", "Social Media", "Google Analytics"],
        "certifications": ["Certified Digital Marketer", "SEO Specialist"]
    },
    {
        "role": "Sales Representative",
        "name": "Emily Davis",
        "contact": {"email": "emily.davis@example.com", "phone": "444-789-0123", "address": "321 Oak St, Anytown, USA"},
        "experience": [
            {"title": "Senior Sales Representative", "company": "Retail Pros", "years": "2018-Present", "description": "Exceeded sales targets and managed client relationships."},
            {"title": "Sales Associate", "company": "Shop Smart", "years": "2015-2018", "description": "Assisted customers and processed sales transactions."}
        ],
        "education": [
            {"degree": "BBA in Business Administration", "institution": "Commerce College", "years": "2011-2015"}
        ],
        "skills": ["Customer Service", "Sales Strategy", "CRM", "Negotiation"],
        "certifications": ["Certified Sales Professional", "Customer Relationship Management"]
    },
    {
        "role": "Graphic Designer",
        "name": "Robert Brown",
        "contact": {"email": "robert.brown@example.com", "phone": "222-333-4444", "address": "654 Pine St, Anytown, USA"},
        "experience": [
            {"title": "Senior Graphic Designer", "company": "Design Hub", "years": "2019-Present", "description": "Designed visual content for various media platforms."},
            {"title": "Graphic Designer", "company": "Creative Studio", "years": "2016-2019", "description": "Created graphics and layouts for product illustrations and websites."}
        ],
        "education": [
            {"degree": "BA in Graphic Design", "institution": "Art Institute", "years": "2012-2016"}
        ],
        "skills": ["Adobe Photoshop", "Illustrator", "InDesign", "Sketch"],
        "certifications": ["Certified Graphic Designer", "Adobe Creative Suite Expert"]
    },
    {
        "role": "Project Manager",
        "name": "Lisa Miller",
        "contact": {"email": "lisa.miller@example.com", "phone": "111-222-3333", "address": "789 Birch St, Anytown, USA"},
        "experience": [
            {"title": "Senior Project Manager", "company": "Enterprise Solutions", "years": "2017-Present", "description": "Led project teams and ensured timely project delivery."},
            {"title": "Project Coordinator", "company": "Business Inc.", "years": "2013-2017", "description": "Assisted in planning and coordinating project activities."}
        ],
        "education": [
            {"degree": "MBA in Project Management", "institution": "Business School", "years": "2011-2013"},
            {"degree": "BA in Management", "institution": "State University", "years": "2007-2011"}
        ],
        "skills": ["Project Planning", "Risk Management", "Agile Methodologies", "MS Project"],
        "certifications": ["PMP", "Certified Scrum Master"]
    },
    {
        "role": "Financial Analyst",
        "name": "Kevin Wilson",
        "contact": {"email": "kevin.wilson@example.com", "phone": "333-444-5555", "address": "987 Cedar St, Anytown, USA"},
        "experience": [
            {"title": "Senior Financial Analyst", "company": "Finance Corp", "years": "2018-Present", "description": "Conducted financial analysis and provided investment recommendations."},
            {"title": "Financial Analyst", "company": "Wealth Management", "years": "2015-2018", "description": "Analyzed financial data and prepared reports."}
        ],
        "education": [
            {"degree": "MSc in Finance", "institution": "Finance University", "years": "2013-2015"},
            {"degree": "BSc in Economics", "institution": "State University", "years": "2009-2013"}
        ],
        "skills": ["Financial Analysis", "Excel", "Forecasting", "Data Analysis"],
        "certifications": ["CFA", "Certified Financial Planner"]
    },
    {
        "role": "Human Resources Manager",
        "name": "Nancy Clark",
        "contact": {"email": "nancy.clark@example.com", "phone": "666-777-8888", "address": "123 Spruce St, Anytown, USA"},
        "experience": [
            {"title": "HR Manager", "company": "Tech Solutions", "years": "2018-Present", "description": "Managed recruitment and employee relations."},
            {"title": "HR Specialist", "company": "Global Inc.", "years": "2014-2018", "description": "Assisted with HR functions and benefits administration."}
        ],
        "education": [
            {"degree": "MBA in Human Resources", "institution": "Business School", "years": "2012-2014"},
            {"degree": "BA in Psychology", "institution": "State University", "years": "2008-2012"}
        ],
        "skills": ["Recruitment", "Employee Relations", "HRIS", "Talent Management"],
        "certifications": ["PHR", "SHRM-CP"]
    },
    {
        "role": "Business Analyst",
        "name": "David Martinez",
        "contact": {"email": "david.martinez@example.com", "phone": "999-000-1111", "address": "456 Maple St, Anytown, USA"},
        "experience": [
            {"title": "Senior Business Analyst", "company": "Consulting Group", "years": "2019-Present", "description": "Analyzed business processes and recommended improvements."},
        ]
    }
] 



# Create and save resumes
file_paths = []
for i, data in enumerate(resumes_data):
    resume_pdf = create_resume(data['role'], data['name'], data['contact'], data['experience'], data['education'], data['skills'], data['certifications'])
    file_path = f"resume_{i+1}.pdf"
    resume_pdf.output(file_path)
    file_paths.append(file_path)

file_paths
