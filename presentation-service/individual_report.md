# Individual Mini-Project Report

**Project Title:** Creator Cloud Studio  
**Module:** Cloud Computing Module - Mini-Project 1  
**Submission Type:** Individual Report

## Abstract

My role in the group project was user-facing integration. I delivered the Presentation Service container that accepts poster submissions, sends them to the workflow layer, and displays the returned result. I also supported the result-update path by defining how final status data should be exposed back to the interface. My work focused on input handling, response parsing, containerisation, and integration with the wider hybrid cloud workflow.

## I. Individual Role and Responsibilities

### A. What I was responsible for

I was responsible for the part of the system that users interact with directly, together with the logic that connects that interface to the rest of the cloud workflow. The main component I delivered was the Presentation Service container. In practice, this meant building a Flask application that provides a submission form, converts user input into the JSON contract expected by the Workflow Service, and renders the final result returned from the downstream processing pipeline.

My work also included interface-level validation to reduce obviously invalid submissions before they reached the backend, while still respecting the rule that the final decision must be produced by the serverless processing flow. I therefore added required fields, a minimum description length, and a filename pattern check in the HTML form, but these checks were only preliminary.

In the wider group system, my responsibility also covered the logic-end integration for returning processed outcomes to the user. That included handling structured responses from the workflow layer, extracting the submission ID, status, and explanatory note, and displaying the result clearly. This connected my work to the Result Update Function, because the frontend needed a consistent status format after background processing completed.

### B. Artefacts I worked on

- `app.py`: Flask routes, request handling, payload construction, workflow API call, response parsing, and error handling.
- `templates/index.html`: submission form UI, field constraints, and front-end input guidance.
- `templates/result.html`: result page showing status, message, submission ID, submitted payload, and raw backend response.
- `Dockerfile`: container packaging for the Presentation Service.
- `requirements.txt`: Python runtime dependencies for Flask and HTTP requests.
- Result-update integration contract: the status/message structure expected by the frontend after background processing.

### C. Integration with the group system

My work sat at the boundary between the user and the rest of the six-component architecture. First, the Presentation Service had to send a correctly structured JSON payload to the Workflow Service, so I aligned the frontend fields with the backend contract and made sure the submission endpoint forwarded `title`, `description`, and `filename` unchanged. Second, the result page had to make sense of what came back from the distributed workflow. Because serverless components may return nested payloads, I implemented parsing logic that could still extract the final status and note.

This meant my code depended on decisions made by the teammates who implemented the Workflow Service, Processing Function, and Data Service. At the same time, their components depended on my interface sending clean input and displaying the final outcome correctly. My contribution was therefore not isolated UI work; it was the integration layer that made the workflow visible and testable from the user side.

## II. Use of Generative AI in My Task

### A. GenAI Tools Used

I used Generative AI as a support tool rather than as a system generator. The main tools I used were a conversational AI assistant and code-completion support for short implementation tasks. I used them to clarify the project rules, scaffold parts of the Flask application, debug integration issues, and review whether my implementation matched the required workflow.

### B. Concrete Examples of GenAI Use

One concrete example was the initial implementation of the Presentation Service form and submission route. I asked GenAI to help me turn the project brief into a minimal Flask application with one page for user input and one page for displaying the result. The useful part of the answer was the basic scaffolding: a route for `/`, a POST route for `/submit`, and an HTML form with fields for title, description, and filename. It also suggested using HTML attributes such as `required`, `minlength`, and a filename pattern to catch obvious errors early. I accepted that structure because it matched the project requirements and reduced repetitive setup work. However, I modified the output: the client-side checks remained only convenience checks, and I changed the wording and page structure so the service aligned with the group system rather than behaving like a standalone validator.

The second example was the response-handling logic in `app.py`. During integration, the assumption that the workflow layer would return a flat JSON object turned out to be too weak. I asked GenAI to suggest a way to parse responses that might contain an outer status code and an inner JSON body. The suggestion was useful because it pointed me toward a dedicated parser function instead of mixing parsing logic into the route itself. I accepted the idea of a separate parser and JSON decoding when the body arrives as a string. However, I did not copy the answer unchanged. I added type checks, fallback handling for malformed JSON, separate tracking of the HTTP status code and the service status code, and storage of the raw response for debugging.

### C. Verification and Critical Evaluation

I treated every AI suggestion as a draft that needed technical verification. My first verification step was to compare the generated or suggested code against the assignment brief. I checked that the user-facing form contained exactly the required fields and that the service did not replace the required serverless processing with local business logic. This mattered because AI often proposes a convenient solution, but convenience is not the same as compliance.

My second verification step was code-level inspection. For the form page, I checked that the description length and filename extension checks matched the project rules. For the Flask route, I checked that the submitted payload preserved the expected keys and that the timeout and exception handling were reasonable for a service-to-service HTTP call. For the result page, I reviewed whether the displayed data would help me understand normal and failure cases during integration.

The most important verification happened around response parsing. Instead of trusting the first AI suggestion, I traced the possible shapes of the returned JSON and designed `parse_response_payload` so it could handle a wrapped body, a direct body, or an unexpected raw value. This mattered because hybrid systems often fail at boundaries rather than inside individual components. GenAI provided speed; my own judgement decided what was safe enough to keep and what assumptions had to be removed.

### D. Limitations and Failures of GenAI

A clear limitation of GenAI in this task was that it sometimes optimised for a neat local solution rather than the specific architecture required by the assignment. In one iteration, the AI suggested handling most validation directly inside the Presentation Service and returning the final outcome from the web app itself. That would have been simpler to implement, but it would have violated the required workflow in which the serverless processing path computes the final result. I detected the problem by rereading the assignment brief.

Another weakness was overconfidence about response formats. AI initially assumed that the backend would return a flat JSON object containing fields such as `status` and `id`. In practice, cloud functions often return a wrapped payload, sometimes with the real body encoded as a JSON string. If I had accepted the first suggestion without checking, the UI could have displayed incomplete or misleading data. I fixed this by separating transport-level and application-level parsing.

The main lesson I learned is that GenAI is strongest when used to accelerate routine implementation patterns, but weakest when precise system constraints and integration contracts matter. In those cases, careful reading of the brief and explicit verification matter more than fluent generated text.

## III. Reflection on Learning

This mini-project improved my understanding of hybrid cloud design by forcing me to think about where each responsibility should live. The Presentation Service was a good fit for a container because it provides a continuously available web interface, depends on a predictable runtime, and benefits from stable packaging with Flask and its dependencies. In contrast, the processing and result-update stages are better suited to serverless execution because they are event-driven and triggered by workflow transitions.

I also learned that integration work in a group project is highly technical even when it looks simple from the outside. A form page is not just a visual component; it is an agreement about field names, validation boundaries, response formats, and failure handling. Small mismatches at those boundaries can make a distributed system appear broken even when each component works in isolation. This made communication with teammates important when aligning payload structure and interpreting returned statuses.

Another important lesson concerned responsible GenAI use. AI helped me move faster when generating boilerplate, reviewing implementation options, and suggesting debugging directions. However, the parts that mattered most still depended on my judgement: checking the precedence of `INCOMPLETE`, `NEEDS REVISION`, and `READY`, preserving the required architecture, and making the frontend robust to real integration behaviour instead of idealised examples. If I repeated the task, I would define the response schema for all components earlier and document it more formally.

## References

1. Mini-Project 1 brief, *Cloud Execution Models (Containers and Serverless)*.
2. Flask documentation: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
3. Requests documentation: [https://requests.readthedocs.io/](https://requests.readthedocs.io/)
