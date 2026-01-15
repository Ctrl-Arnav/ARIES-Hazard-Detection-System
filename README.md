 # ARIES

Advanced Real-Time Intelligence & Emergency System

Existing safety sensors are reactive and context-blind. ARIES turns "dumb" camera infrastructure into a proactive, intelligent emergency grid that understands not just that a hazard is happening, but how severe it is and who is at risk.

 
Going beyond simple "Hazard Detection"

Most AI safety projects simply draw boxes around fires or similar hazards. ARIES introduces three core innovations that solve real-world emergency response problems:

### 1. The Intelligence Gate (Resource-Aware AI)

In a disaster, hardware is often limited. ARIES uses Gated Inference logic:

 A lightweight model constantly monitors for primary threats (Fire/Smoke).

And heavy models (PPE Compliance/First Responder Tracking) stay "dormant" and only activate once a hazard is confirmed.



### 2. Severity-Based Logic (The "HZRD" Class)

We specialized the model to minimalize the risk of False Positives. Since all types of fires do not pose a threat, we trained our model to distinguish based on severity

🟢fire : Small, contained flames.

🔴 HZRD: High-risk violent flames with uneven shape and heavy smoke.



### 3. Human-Hazard Correlation

ARIES considers if the hazard is near an unprotected person? By fusing PPE Detection with Fire Proximity, it identifies when a person is in a "Red Zone" without a helmet or vest, providing a higher level of situational awareness.

ARIES is intentionally deployed as a web-hosted system, not a closed local application.
This design choice is critical to its role as an emergency intelligence layer, not just a detection model.

From Isolated Cameras to a Connected Emergency Grid

Traditional safety cameras are: isolated, viewable only on-site

By hosting ARIES as a web-accessible system, we transform existing camera infrastructure into a shared, intelligent emergency grid.

Website hosting enables:

Centralized situational awareness
Multiple camera feeds (webcams, uploaded footage, remote devices) can be analyzed through a single backend.

Device-agnostic access
Any authorized responder can view analytics from:

control rooms,
laptops,
tablets,
low-power edge terminals
without installing specialized software.

Real-time decision support
Instead of raw video, responders receive:

severity-aware alerts,
hazard area coverage,
human–hazard context
directly in the browser.



## System Architecture & Design

The system is built on a Modular FastAPI Pipeline—moving away from monolithic designs to ensure each component can scale independently.

Logic-Driven Backend: A custom Inference Compiler that handles the "Gating" logic before frames are even processed.

Zero-Overhead Frontend: A vanilla JS/HTML5 Canvas interface. By avoiding heavy frameworks like Gradio for the final UI, we reduce latency and give responders a "clean" view.

Edge-Ready: Designed to run on CPU-only tiers (Hugging Face / Smart City Nodes), proving that life-saving AI doesn't require a $10,000 GPU.



## Tech Stack

AI Engine: YOLOv8 (Custom-trained for HZRD, Smoke, and PPE classes).

Backend: FastAPI (Asynchronous frame processing), HuggingFace.

Frontend: HTML5 Canvas (Low-latency rendering).

Logic: Conditional Inference Gating.

--

## Co-authors
* https://github.com/kokomelone
* https://github.com/VanshikaMahindru



