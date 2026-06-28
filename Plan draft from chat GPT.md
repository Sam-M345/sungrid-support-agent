SunGrid Support Agent, AI Portfolio Project Plan

Introduction, What We Are Building and Why
The purpose of this project is to create a strong, recruiter-facing AI portfolio project that helps me stand out for roles such as AI Engineer, Applied AI Engineer, AI Deployment Engineer, Customer Engineer, Solutions Engineer, AI Success Engineer, Forward Deployed Engineer, and Technical AI Consultant.
This is not meant to be a large software engineering project. The goal is not to prove that I can build a complex production app with advanced backend infrastructure. The goal is to show that I can identify a realistic business problem, design an applied AI solution, build a working prototype, explain the workflow clearly, demonstrate RAG and agentic AI patterns, deploy the project online, and present it in a way that is easy for recruiters and hiring managers to understand.
The final project should make my portfolio, GitHub, LinkedIn profile, and resume more attractive to recruiters. Ideally, someone should be able to open the live demo, ask a realistic customer question, see the AI-generated answer, understand which documents were used, and see the steps the system followed to produce the answer.
The project will be called SunGrid Support Agent. It will be built for a fictional solar company called SunGrid Solutions. The assistant will help customer support reps answer homeowner questions about warranty, troubleshooting, safety escalation, and financing by using trusted internal company documents.
The final outcome will include a working Streamlit app, a GitHub repository, synthetic company documents, a Miro visual board, LangSmith tracing evidence, screenshots, a LinkedIn launch post, and a resume-ready project bullet.
________________________________________
1. Main Project Goal
Build a recruiter-facing applied AI portfolio project called SunGrid Support Agent for a fictional solar company called SunGrid Solutions.
The project should demonstrate:
•	Applied AI solution design
•	Business problem framing
•	RAG over internal company documents
•	LangChain usage
•	LangGraph workflow orchestration
•	LangSmith observability
•	Claude API integration
•	Risk-based escalation
•	Human-in-the-loop thinking
•	Streamlit deployment
•	Visual explanation through Miro
•	Clear GitHub documentation
•	LinkedIn-ready portfolio presentation
The final project should show that I can take a real business problem and design a practical AI workflow around it.
________________________________________
2. Business Problem
SunGrid Solutions is a fictional solar company whose customer support team receives many questions from homeowners about warranty coverage, low energy production, monitoring issues, inverter problems, safety concerns, and financing terms.
Support reps currently spend too much time manually searching through warranty policies, troubleshooting guides, safety procedures, financing FAQs, and support SOPs. This creates slow response times, inconsistent answers, unnecessary escalations, and higher risk when dealing with technical, safety, warranty, or financing-related questions.
The project solves this by building an AI assistant that helps support reps answer customer questions using trusted internal company documents. The assistant retrieves relevant source material, drafts a customer-ready response, creates an internal support note, shows sources, scores risk and confidence, and recommends whether the case should be escalated.
________________________________________
3. Main User
The main user is a customer support rep at SunGrid Solutions.
The input questions will be written from the homeowner/customer perspective, but the assistant’s output will be designed to help the support rep respond.
Example customer question:
“My panels are producing much less energy than expected. Is this covered under warranty?”
The assistant will return:
•	Customer-ready response
•	Internal support note
•	Sources used
•	Risk level
•	Confidence score
•	Escalation recommendation
•	Workflow trace
•	Retrieved document chunks
________________________________________
4. Final Project Scope
The assistant will support four main categories:
•	Warranty questions
•	Troubleshooting questions
•	Safety escalation questions
•	Financing FAQ questions
We will not include product recommendations in the first version. That keeps the project focused, useful, and manageable.
The goal is to build a polished applied AI demo, not an overly complex software product.
________________________________________
5. Core Technology Stack
Area	Tool
Main language	Python
LLM	Claude API
Framework	LangChain
Workflow orchestration	LangGraph
Vector database	Chroma
Observability	LangSmith
Demo interface	Streamlit
Visual planning	Miro
Repository	GitHub
Deployment	Streamlit Community Cloud
Local secrets	.env file
Online secrets	Streamlit Secrets
________________________________________
6. Synthetic Company Documents
Because SunGrid Solutions is fictional, we will create synthetic company documents ourselves. These documents will be realistic enough to support RAG, but not so long that the project becomes too complex.
Planned document folder:
/docs
  warranty_policy.md
  installation_troubleshooting_guide.md
  safety_escalation_policy.md
  customer_support_sop.md
  financing_faq.md
warranty_policy.md
This document will cover:
•	Panel performance warranty
•	Inverter warranty
•	Battery warranty
•	Warranty exclusions
•	Required claim documentation
•	Performance degradation rules
•	When support should escalate to warranty review
installation_troubleshooting_guide.md
This document will cover:
•	Low energy output checklist
•	Monitoring app issues
•	Inverter alert codes
•	Shading and weather checks
•	Recent storm checks
•	Technician visit criteria
safety_escalation_policy.md
This document will cover:
•	Burning smell near inverter
•	Exposed wiring
•	Battery overheating
•	Electrical shock risk
•	Fire risk
•	Roof damage
•	When to stop troubleshooting and escalate immediately
customer_support_sop.md
This document will cover:
•	How to classify incoming questions
•	How to ask follow-up questions
•	When to answer directly
•	When to escalate
•	How to document the case
•	How to communicate uncertainty
financing_faq.md
This document will cover:
•	Monthly payment questions
•	Lease vs. ownership
•	Cancellation windows
•	Tax credit disclaimer
•	Billing issues
•	When to refer to the financing team
The app and README should include a short disclaimer:
“Demo note: This is a synthetic portfolio project using fictional company documents. Not real solar, warranty, safety, or financial advice.”
________________________________________
7. RAG Workflow
RAG will be used to make the assistant answer from SunGrid’s internal documents instead of relying only on the general knowledge of the language model.
The RAG process will work like this:
1.	Load the synthetic company documents.
2.	Split documents into smaller chunks.
3.	Create embeddings for each chunk.
4.	Store the chunks in Chroma.
5.	Receive a customer question.
6.	Retrieve the most relevant chunks.
7.	Send the retrieved context to Claude.
8.	Generate a grounded answer.
9.	Show the source documents and retrieved chunks in the app.
The app should clearly demonstrate that RAG was used by showing:
•	Source document names
•	Section titles
•	Retrieved chunks
•	Final answer based on those chunks
This is important because recruiters should be able to see that the response did not come from a generic chatbot. It came through a structured system using internal documents.
________________________________________
8. LangChain Usage
LangChain will be used to connect the main AI components.
LangChain will help with:
•	Claude model connection
•	Document loading
•	Text splitting
•	Embedding creation
•	Chroma retriever connection
•	Prompt templates
•	RAG chain setup
•	Output formatting
LangChain’s role is to show that I can build a practical AI application using tools that are relevant to customer-facing AI and applied AI deployment roles.
________________________________________
9. LangGraph Workflow
LangGraph will control the step-by-step logic of the assistant.
Main workflow:
Customer Question
↓
Intent Classification
↓
Document Retrieval
↓
Answer Generation
↓
Answer Validation
↓
Risk Scoring
↓
Final Answer or Human Escalation
Normal Path
Question
→ Classify intent
→ Retrieve relevant documents
→ Generate answer
→ Validate answer
→ Assign low/medium risk
→ Return answer
High-Risk Path
Question
→ Classify as safety risk
→ Retrieve safety policy
→ Generate limited safe response
→ Assign high risk
→ Escalate to human
This is one of the most important parts of the project because it shows that the assistant is not just a chatbot. It is a structured AI workflow with decision points.
________________________________________
10. Risk and Escalation Behavior
The assistant should answer normal questions, but escalate or refuse when the question is too risky.
It should escalate or refuse when the question involves:
•	Burning smell
•	Electrical shock
•	Exposed wiring
•	Battery overheating
•	Fire risk
•	Roof damage
•	Unsafe repair instructions
•	Legal guarantees
•	Financial promises
•	Unsupported claims not found in the documents
Example high-risk output:
Customer-ready response:
Because you mentioned a burning smell near the inverter, please stop interacting with the equipment and contact SunGrid support immediately. This issue requires escalation to a qualified technician.

Internal support note:
Issue type: Safety escalation
Risk level: High
Action: Escalate immediately
Reason: Safety policy prohibits remote troubleshooting for potential electrical hazards.
This demonstrates responsible AI design and human-in-the-loop thinking.
________________________________________
11. Streamlit App Design
The Streamlit app should be simple, visual, and recruiter-friendly.
It should feel like a working AI demo, not just a code project.
Main Sections
1. Project Header
Include:
•	SunGrid Support Agent
•	Short explanation of what it does
•	Very short demo disclaimer
Example:
“SunGrid Support Agent helps solar customer support reps answer homeowner questions using synthetic company documents, RAG, LangGraph workflow routing, and risk-based escalation.”
2. Sample Questions Box
A visible box with clickable sample questions.
The goal is to help recruiters quickly test the demo without needing to think of their own question.
3. Free-Text Input Box
Users should also be able to type their own customer question.
4. Customer-Ready Response
A polished answer that a support rep could send to the homeowner.
5. Internal Support Note
A structured internal note for the support rep.
Fields:
Issue type:
Risk level:
Confidence:
Sources used:
Recommended action:
Escalation needed:
6. Sources Used
Show which documents supported the answer.
Example:
Sources:
1. Warranty Policy, Section 3.2, Performance Degradation
2. Troubleshooting Guide, Section 2.1, Low Output Checklist
3. Customer Support SOP, Section 4.3, Warranty Escalation
7. Dynamic Workflow Trace
Show the steps the system followed for each answer.
Example:
✅ Step 1: Classified as Warranty + Troubleshooting
✅ Step 2: Retrieved 3 document chunks
✅ Step 3: Generated grounded answer
✅ Step 4: Validated citations
✅ Step 5: Risk level: Medium
✅ Step 6: Escalation: Not immediate
For safety cases:
✅ Step 1: Classified as Safety Risk
✅ Step 2: Retrieved Safety Escalation Policy
✅ Step 3: Generated limited safe response
✅ Step 4: Risk level: High
✅ Step 5: Escalation required
8. Retrieved Context Section
Use an expandable section called:
“View retrieved context”
This will show the actual document chunks retrieved by RAG.
This is important because it proves the answer came from the system’s document retrieval process.
________________________________________
12. Sample Questions
The sample questions should be written from the homeowner/customer perspective.
Possible sample questions:
1.	“My panels are producing about 35% less energy than expected. Is this covered under warranty?”
2.	“My monitoring app stopped showing production data. Does that mean my system is broken?”
3.	“I smell something burning near the inverter. What should I do?”
4.	“Can I cancel my solar financing agreement after installation?”
5.	“My inverter is showing an error code after a storm. Should I reset it?”
6.	“My bill is higher than expected even though I have solar panels. Why?”
7.	“There are exposed wires near the panel connection box. Can I tape them myself?”
8.	“What information do I need before starting a warranty claim?”
These questions should demonstrate normal answers, missing-information handling, RAG retrieval, and risk escalation.
________________________________________
13. Output Format After Each Answer
Each answer should include four major parts.
1. Customer-Ready Response
A polished response the support rep could send to the homeowner.
2. Internal Support Note
A structured note for the support rep.
Example:
Issue type: Warranty + Troubleshooting
Risk level: Medium
Confidence: 82%
Sources used: Warranty Policy, Troubleshooting Guide, Customer Support SOP
Recommended action: Ask diagnostic questions first, then escalate if unresolved
Escalation needed: Not immediate
3. Sources Used
Show the document names and sections.
4. Retrieved Document Chunks
Hidden inside an expandable section.
This makes the project more transparent and helps recruiters understand that the system uses RAG.
________________________________________
14. LangSmith Usage
LangSmith should be included in the implementation.
Use LangSmith to:
•	Trace each app run
•	Inspect LangGraph steps
•	Track retrieved documents
•	Debug prompts
•	Inspect model outputs
•	Save screenshots for GitHub
•	Show observability and evaluation evidence
The GitHub README should include:
•	LangSmith trace screenshot
•	Explanation of what the trace shows
•	Example of successful retrieval
•	Example of high-risk escalation
This is important because it shows deployment and debugging maturity, not just prompt writing.
________________________________________
15. Miro Visual Board
Miro will be used for the polished visual story.
We will create one universal flowchart for the full project. We will not call Miro dynamically for every question.
Miro Board Sections
1. Business Problem Map
Show:
•	Slow support responses
•	Inconsistent answers
•	Manual document search
•	Warranty risk
•	Safety escalation risk
•	Financing confusion
2. User Journey
Show:
Homeowner asks question
→ Support rep enters question
→ AI assistant retrieves documents
→ Assistant drafts response
→ Support rep reviews and responds
3. RAG Architecture
Show:
Synthetic docs
→ Chunking
→ Embeddings
→ Chroma vector database
→ Retriever
→ Claude
→ Source-backed answer
4. LangGraph Workflow
Show:
Classify
→ Retrieve
→ Generate
→ Validate
→ Risk score
→ Answer or escalate
5. Human Escalation Path
Show when escalation happens:
•	Safety risk
•	Low confidence
•	Unsupported claim
•	Financial/legal promise
•	Missing information
6. Recruiter Explanation Section
Show what the project demonstrates:
•	Applied AI
•	RAG
•	LangGraph
•	LangSmith
•	Risk-based escalation
•	Business problem solving
•	Deployment-ready thinking
The Miro board should be linked in GitHub and LinkedIn.
________________________________________
16. GitHub Repository Plan
Recommended repo name:
sungrid-support-agent
Suggested repo structure:
sungrid-support-agent/
  app.py
  README.md
  requirements.txt
  .gitignore
  .env.example

  docs/
    warranty_policy.md
    installation_troubleshooting_guide.md
    safety_escalation_policy.md
    customer_support_sop.md
    financing_faq.md

  src/
    config.py
    document_loader.py
    vector_store.py
    retriever.py
    prompts.py
    graph.py
    risk_scoring.py
    validation.py
    response_formatter.py

  examples/
    sample_questions.md
    evaluation_cases.md

  assets/
    architecture_diagram.png
    langgraph_workflow.png
    streamlit_screenshot.png
    langsmith_trace_screenshot.png
GitHub README Should Include
1.	Project title
2.	Short demo summary
3.	Business problem
4.	Why this project exists
5.	Solution overview
6.	Tools used
7.	Architecture diagram
8.	LangGraph workflow
9.	RAG explanation
10.	Streamlit screenshots
11.	Sample outputs
12.	LangSmith screenshot
13.	How to run locally
14.	How to deploy
15.	Limitations
16.	Future improvements
17.	Live demo link
18.	Miro board link
19.	LinkedIn post link, once published
________________________________________
17. Local Development Steps
High-level build order:
1.	Create the local project folder.
2.	Create the GitHub repository.
3.	Set up the folder structure.
4.	Create the synthetic SunGrid documents.
5.	Create .env.
6.	Add Claude API key locally.
7.	Add LangSmith environment variables.
8.	Add .env to .gitignore.
9.	Create .env.example.
10.	Build document loading.
11.	Build document chunking.
12.	Build Chroma vector store.
13.	Build retriever.
14.	Build prompts.
15.	Build LangGraph workflow.
16.	Add risk scoring.
17.	Add answer validation.
18.	Add response formatting.
19.	Build Streamlit interface.
20.	Add sample question buttons.
21.	Add free-text input.
22.	Add workflow trace display.
23.	Add retrieved context section.
24.	Test all sample questions.
25.	Capture screenshots.
26.	Update README.
27.	Push to GitHub.
________________________________________
18. Deployment Plan
Use Streamlit Community Cloud.
Deployment steps:
1.	Push the finished project to GitHub.
2.	Create or open Streamlit Community Cloud.
3.	Connect Streamlit to the GitHub repository.
4.	Select app.py as the main file.
5.	Add secrets in Streamlit Secrets:
o	ANTHROPIC_API_KEY
o	LangSmith keys/settings
6.	Deploy the app.
7.	Test the public link.
8.	Confirm sample questions work.
9.	Confirm custom questions work.
10.	Confirm sources display.
11.	Confirm risk/confidence display.
12.	Confirm workflow trace display.
13.	Confirm retrieved context display.
14.	Add the Streamlit link to GitHub README.
15.	Add the Streamlit link to resume/portfolio.
16.	Use the Streamlit link in the LinkedIn post.
Recommended public app URL style:
sungrid-support-agent.streamlit.app
We will keep deployment simple and use a Streamlit URL instead of buying a separate custom domain.
________________________________________
19. Recruiter-Facing Polish
The project should look like a complete applied AI case study, not just a code repository.
Must-have polish items:
•	Clean GitHub README
•	Streamlit live app
•	Miro board
•	Architecture diagram
•	Sample questions
•	Screenshots
•	LangSmith trace screenshot
•	Clear business problem
•	Clear explanation of RAG
•	Clear explanation of LangGraph
•	Clear explanation of escalation and guardrails
•	Short LinkedIn post
•	Resume bullet
The recruiter should quickly understand:
•	What problem the project solves
•	Who the user is
•	How the AI system works
•	What tools were used
•	Why this is relevant to customer-facing applied AI roles
________________________________________
20. LinkedIn Launch Plan
Once the project is complete, publish a LinkedIn post.
The LinkedIn post should include:
•	Business problem
•	What I built
•	Tools used
•	Why it matters
•	Live Streamlit demo link
•	GitHub repo link
•	Miro board or architecture image
•	Screenshot or short demo video
•	Note that it is a synthetic portfolio project
Suggested LinkedIn angle:
“I built SunGrid Support Agent, an applied AI deployment demo for a fictional solar company. It uses Claude, LangChain, LangGraph, Chroma, RAG, LangSmith, and Streamlit to help customer support reps answer warranty, troubleshooting, safety, and financing questions from internal company documents. The app shows the answer, sources, retrieved context, workflow path, confidence, risk level, and escalation recommendation.”
The post should emphasize:
•	Applied AI
•	Customer-facing workflow
•	RAG with citations
•	Agentic workflow
•	Risk-based escalation
•	Live demo
•	Business value
•	Recruiter-friendly communication
________________________________________
21. Resume Bullet After Completion
Possible resume bullet:
SunGrid Support Agent | LangChain, LangGraph, Claude, Chroma, LangSmith, Streamlit
Built and deployed a recruiter-facing AI support assistant for a fictional solar company, using RAG over synthetic warranty, troubleshooting, safety, and financing documents. Designed a LangGraph workflow for intent classification, document retrieval, grounded answer generation, validation, risk scoring, and human escalation, with LangSmith tracing and a live Streamlit demo showing sources, workflow steps, confidence, and retrieved context.
________________________________________
22. Interview Talking Points
In interviews, I should be able to explain:
•	Why I chose this business problem
•	Why RAG was needed
•	Why LangGraph was useful
•	How LangChain connected the AI components
•	How LangSmith helped with observability
•	How the assistant handles risky questions
•	How the system avoids unsupported answers
•	How support reps would use it
•	What I would improve in a real deployment
•	How this relates to customer-facing applied AI work
Strong interview summary:
“I built SunGrid Support Agent to show how an AI assistant can support a real business workflow. The system helps solar support reps answer homeowner questions using internal documents. It uses RAG to ground answers, LangGraph to control workflow decisions, LangSmith for tracing, and Streamlit for a live demo. The app also shows sources, retrieved context, confidence, risk level, and escalation recommendations so the answer is explainable and not just a black-box chatbot.”
________________________________________
23. What We Should Avoid
To keep the project manageable and aligned with applied AI roles, we should avoid:
•	Real user login
•	Real CRM integration
•	Real payment system
•	Real customer database
•	Complex backend
•	Complex frontend
•	Multi-user permissions
•	Real solar engineering calculations
•	Real warranty/legal/financial advice
•	Full production infrastructure
•	Overcomplicated product recommendation engine
•	Too many features
This project should stay focused on applied AI, RAG, workflow design, deployment, communication, and recruiter-facing presentation.
________________________________________
24. Final Deliverables
At the end, the project should include:
1.	GitHub repository
o	Code, docs, README, screenshots, setup instructions
2.	Live Streamlit app
o	Recruiters can type a question and test it
3.	Miro board
o	Visual business and architecture explanation
4.	Synthetic company documents
o	Warranty, troubleshooting, safety, support SOP, financing FAQ
5.	LangSmith evidence
o	Traces and screenshots
6.	LinkedIn post
o	Recruiter-facing project announcement
7.	Resume bullet
o	Added to AI projects section
8.	Interview story
o	Clear explanation of business problem, architecture, tradeoffs, and results
________________________________________
25. Final Project Positioning
The final story should be:
“I built SunGrid Support Agent to demonstrate how a customer-facing AI system can help a solar company’s support reps answer customer questions using trusted internal documents. The system uses RAG for grounded answers, LangGraph for workflow control, LangSmith for observability, Claude as the LLM, Chroma as the vector database, and Streamlit for a live deployed demo. It shows the answer, the sources, the workflow path, the retrieved context, the confidence level, the risk level, and whether escalation is required.”
This is the right level of complexity. It is practical, visual, deployable, and recruiter-friendly without becoming a full software engineering project.
