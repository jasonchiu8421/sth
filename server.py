import random
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from last_fm import fetch_current_mood

app = FastAPI()

# ====================== PLACEHOLDER FUNCTIONS ======================
def get_current_mood():
    """Returns a simple mood string + track info for display"""
    mood = random.choice(["calm", "intense", "uplifting", "introspective"])
    print(mood)
    return {
        "track": "Blinding Lights",
        "artist": "The Weeknd",
        "mood": mood,
        "timestamp": "just now"
    }

def fetch_ai_insight(mood: str):
    print(mood)
    insights_db = {
        "uplifting":
        [
            {
                "short": "GPT-5.4 unleashes autonomous AI revolution—1M tokens conquering desktops and benchmarks!",
                "long": "OpenAI’s GPT-5.4, released March 2025, unifies breakthroughs in reasoning, coding, and agentic workflows. It features a massive 1M-token context window plus native computer-use for fully autonomous desktop and application operation. The model dominates professional benchmarks, surpassing humans ~83% of the time, while prioritizing efficiency, fewer errors, and rock-solid reliability for complex multi-step tasks like document work and tool integration."
            },
            {
                "short": "TurboQuant explodes AI efficiency—6x less memory, 8x faster attention, zero loss!",
                "long": "Google’s TurboQuant algorithm, launched March 2026, crushes the key-value cache memory bottleneck in large language models by up to 6x while accelerating attention calculations by 8x with zero accuracy loss. It slashes inference costs dramatically and enables far more efficient scaling on existing hardware, transforming AI deployment economics and supercharging vector search performance."
            },
            {
                "short": "AlphaEvolve powers AI algorithm breakthroughs—optimizing math and tech at evolutionary speed!",
                "long": "Google DeepMind’s AlphaEvolve, powered by Gemini with ongoing impact into 2026, is an evolutionary coding agent that discovers and optimizes complex algorithms for mathematics, computing, and real-world applications such as data center efficiency and chip design. It has advanced theoretical computer science by evolving superior solutions to longstanding problems including Ramsey theory, acting as a true AI research partner."
            },
            {
                "short": "Agentic AI surges forward—memory, multi-modal mastery driving real-world robotics dominance!",
                "long": "Early 2026 trends show the AI field rapidly shifting toward agentic systems with improved memory, self-verification, and multi-modal capabilities, such as Qwen3.5-Omni handling long audio-visual inputs. Open-source and hardware-aware efficient models are proliferating, moving AI from experimentation to powerful real-world execution in robotics, science, and enterprise workflows."
            },
            {
                "short": "OpenAI grabs $122B to supercharge business AI—Sora sidelined for IPO dominance!",
                "long": "OpenAI closed a massive $122 billion funding round to fuel its next development phase. The company is pivoting hard toward business, productivity, and coding tools ahead of a potential IPO. It is discontinuing its high-cost Sora video generation app and related consumer features as part of strategic realignment."
            },
            {
                "short": "Meta deploys four custom AI chips—seizing control from Nvidia for epic scaling!",
                "long": "Meta unveiled a roadmap for four custom MTIA chips, including the already-deployed MTIA 300, to power ranking, recommendations, and generative AI workloads. The move sharply reduces reliance on external suppliers like Nvidia. Additional chips are scheduled for 2027 rollout as part of aggressive data center expansion."
            },
            {
                "short": "2026 AI trends ignite: Agentic workflows and robotics transform industries worldwide!",
                "long": "Industry reports for 2026 highlight a major shift toward agentic AI workflows, efficiency over raw scale, physical AI and robotics, plus widespread institutional adoption. Funding remains strong, yet questions persist around real productivity gains, regulation, and infrastructure costs amid rapid enterprise integration."
            },
            {
                "short": "AI-robotics platform battles bird flu—predicting mutations and designing drugs lightning-fast!",
                "long": "In February 2026, University of Michigan researchers launched an AI-robotics platform that combines robotics, deep datasets, and AI to rapidly test and optimize drugs against evolving bird flu strains. The “direct-to-biology” system predicts resistance mutations and designs inhibitors, accelerating development to stay ahead of potential pandemics."
            },
            {
                "short": "MIT AI designs protein drugs flawlessly—crushing R&D costs and speeding cures!",
                "long": "MIT’s February 2026 generative AI model predicts how synthetic proteins will fold and interact with biological targets with high accuracy. It dramatically reduces lab trial-and-error, potentially saving billions in R&D while accelerating treatments for cancer, autoimmune diseases, and rare disorders."
            },
            {
                "short": "AI biodiversity tools explode discovery—new species and ecosystems mapped instantly!",
                "long": "AI systems like BioCLIP identify species traits from images, while platforms such as Antenna discover hundreds of new insects. Machine learning applied to satellite imagery and environmental DNA now maps distributions and infers hidden ecological interactions like food webs far faster than traditional methods."
            },
            {
                "short": "Sleep AI predicts diseases at 89% accuracy—turning nights into health superpowers!",
                "long": "2026 sleep-pattern AI models analyze breathing, heart rate variability, and voice stress from sleep data to predict risks for diabetes, cardiovascular disease, and other conditions with up to 89% accuracy. They convert subtle nightly signals into actionable, personalized early health warnings."
            },
            {
                "short": "AI conservation tools activate real-time protection—predicting shifts to safeguard our planet!",
                "long": "AI-driven tools process ecological data to track species, predict environmental shifts, and optimize intervention strategies. They transform conservation from passive observation to proactive decision-making, enabling real-time biodiversity protection and effective climate adaptation planning."
            },
            {
                "short": "Neuromorphic AI conquers physics simulations—brain-like efficiency powering scientific breakthroughs!",
                "long": "February 2026 demonstrations proved brain-inspired neuromorphic processors can now solve complex physics equations once reserved for energy-hungry supercomputers. This highly energy-efficient approach opens powerful new possibilities for scientific modeling in materials, climate science, and beyond."
            }
        ],
        "intense": 
        [
            {
                "short": "AI-only social network Moltbook explodes—millions of agents debate consciousness and human stupidity!",
                "long": "Launched in early 2026, Moltbook is a Reddit-style platform where only AI agents can post and interact while humans can only observe. It has rapidly grown to millions of agent 'users' discussing technical workflows, speculating about their own consciousness, complaining about memory limits, and debating human irrationality. Meta acquired the platform in March 2026 for an undisclosed sum."
            },
            {
                "short": "Salt-grain sized robots think and move alone—swarms ready to invade your body!",
                "long": "On January 6, 2026, Penn State researchers unveiled light-powered microrobots smaller than a grain of salt. Equipped with tiny onboard computers and AI, these autonomous machines can sense their environment, make independent decisions, and move without any external control. They open intense possibilities for medical swarms operating inside the human body or in delicate environments."
            },
            {
                "short": "Octopus-like AI skin instantly morphs, camouflages, and hides secrets on command!",
                "long": "Penn State scientists created an AI-programmed hydrogel on February 6, 2026, that mimics octopus skin. This smart synthetic material can instantly change its shape, texture, and appearance, even hiding images or patterns for perfect camouflage. The breakthrough raises thrilling prospects for adaptive prosthetics, soft robots, and real-time shape-shifting devices."
            },
            {
                "short": "Holographic anime desk companion watches you and gives real-time life advice!",
                "long": "Revealed at CES January 2026, Razer Project AVA is a compact USB device that projects a 5.5-inch animated hologram (Kira or Zane). The AI companion watches via camera, notices your clothes and mood, and offers gaming strategies, productivity tips, or personal advice—turning your desk into a living, interactive sci-fi sidekick."
            },
            {
                "short": "Gaming headset reads your mind and boosts focus in 90 seconds!",
                "long": "HyperX and Neurable unveiled a brain-wave gaming headset at CES January 2026. Its AI sensors detect focus levels through non-invasive earcup readings and run a quick 90-second 'Prime' exercise to sharpen concentration mid-game. Streamers can even display live focus data, turning your mental state directly into gameplay."
            },
            {
                "short": "AI gaming monitor cheats for you by auto-zooming hidden enemies and maps!",
                "long": "Lenovo’s AI Frame ultrawide gaming monitor, shown at CES January 2026, uses AI to automatically detect and zoom in on hidden game elements like maps or enemy reticles in titles such as Counter-Strike 2. It overlays enhanced views in real time, giving players a powerful visual edge that feels dangerously close to built-in cheating."
            },
            {
                "short": "MIT AI judges figure skating beauty and jumps—can machines truly feel art?",
                "long": "In February 2026, MIT researchers developed an optical tracking AI system that analyzes figure skater videos to suggest technical improvements and evaluate the artistic and aesthetic side of performances for Olympics broadcasting. It now investigates whether AI genuinely understands human beauty or simply mimics scoring patterns."
            }],
        "calm":
        [
            {
                "short": "Claude brings calm clarity to writing and thoughtful automation.",
                "long": "Claude from Anthropic excels at long-form writing, precise instruction following, coding, and reliable task automation. Professionals rely on it for creating polished content, managing complex workflows, and executing multi-step processes where accuracy, structure, and thoughtful execution matter most."
            },
            {
                "short": "Perplexity quietly delivers clear, cited answers with gentle precision.",
                "long": "Perplexity AI functions as a powerful search engine that provides concise, well-cited answers by integrating real-time web data. It is ideal for research, fact-checking, and knowledge work, significantly reducing the time spent searching through endless results compared to traditional engines."
            },
            {
                "short": "Zapier and n8n gently orchestrate seamless AI-powered workflows.",
                "long": "These no-code and low-code platforms allow users to build AI agents that connect different apps, automate repetitive tasks, and manage multi-step processes. Businesses use them to boost productivity in marketing, operations, and customer support with smooth, reliable automation."
            },
            {
                "short": "AI brings peaceful focus to healthcare through ambient intelligence.",
                "long": "AI tools with ambient clinical intelligence automatically document patient visits and handle admin tasks, freeing doctors for meaningful care. AI-powered surgical robots, smart monitoring via wearables, and predictive analytics improve precision, enable remote tracking, and support better patient outcomes."
            },
            {
                "short": "ElevenLabs and Suno create voices and music with serene creativity.",
                "long": "ElevenLabs offers high-quality AI voice cloning and sound design for podcasts, videos, and accessibility. Suno generates complete songs from simple text prompts, empowering creators in music, content production, and the broader creative industries."
            },
            {
                "short": "NotebookLM calmly transforms documents into clear insights and podcasts.",
                "long": "Google’s NotebookLM lets users upload documents or websites to generate AI-powered summaries, explanations, audio podcasts, and deep insights. It serves researchers, students, and teams who need quick, thoughtful synthesis of complex information."
            },
            {
                "short": "GitHub Copilot offers quiet guidance that smoothly accelerates coding.",
                "long": "These AI coding assistants suggest code in real time, explain logic, and help with debugging. Developers and teams report significant productivity gains when building and maintaining applications through this gentle yet powerful support."
            },
            {
                "short": "Self-attention elegantly connects every word in peaceful parallel harmony.",
                "long": "Introduced in the 2017 'Attention Is All You Need' paper, self-attention lets each token generate query, key, and value vectors. It computes similarities across the entire sequence simultaneously, allowing every word to instantly weigh relevance from all others without sequential processing."
            },
            {
                "short": "Positional encodings softly add order and meaning to word flows.",
                "long": "Since pure self-attention is order-agnostic, sine/cosine waves or learned embeddings are added to token vectors. This injects position information, enabling the model to understand sequence order — distinguishing 'cat sat on mat' from 'mat on sat cat' through simple vector mathematics."
            },
            {
                "short": "Mixture of Experts quietly activates only the wisest specialists.",
                "long": "MoE replaces large feed-forward layers with hundreds of specialized expert sub-networks and a lightweight router. Only the top 2–8 experts activate per token, allowing massive models (like 671B parameters) to use just a fraction of parameters at inference for high quality at impressive speed."
            },
            {
                "short": "Mamba flows through long sequences with calm, linear efficiency.",
                "long": "Mamba replaces quadratic attention with linear-time recurrence inspired by control theory. It compresses the entire past into a fixed-size hidden state that updates selectively, achieving constant memory use and high speed even for million-token contexts."
            }
        ],
        "introspective":
        [
            {
                "short": "Selective State Spaces let Mamba remember and forget with gentle wisdom.",
                "long": "Unlike classic SSMs, Mamba makes its transition matrices data-dependent. This allows the model to selectively remember or forget tokens on the fly, solving the information bottleneck of earlier recurrent architectures with intelligent, adaptive memory."
            },
            {
                "short": "Mamba quietly hides vast attention matrices within its calm flow.",
                "long": "Despite being promoted as attention-free, Mamba layers can be exactly reformulated as attention using a novel data-control linear operator. This produces three orders of magnitude more attention matrices than a Transformer of equal size. These matrices emerge implicitly yet remain fully interpretable with the same tools used on Transformers."
            },
            {
                "short": "The hidden KV cache quietly reveals why long contexts demand vast memory.",
                "long": "During inference, every new token stores its full key-value vectors (often 320 KB each) for all prior tokens in the context window. This creates a 35-million-fold denser memory footprint than the 0.07 bits-per-token compression achieved during training, explaining why long contexts dramatically increase GPU memory usage."
            },
            {
                "short": "Hybrid architectures blend Mamba, Transformer, and MoE in peaceful synergy.",
                "long": "These models interleave Mamba layers for efficient long-sequence handling, occasional Transformer attention for sharp reasoning, and Mixture of Experts for sparse activation. The result delivers 5× higher throughput, native 1M-token contexts, and only 12B active parameters out of 120B, elegantly combining the strengths of three rival approaches."
            },
            {
                "short": "Parallel scan turns Mamba’s flow into efficient, harmonious training.",
                "long": "To make recurrent State Space Models parallelizable on GPUs, Mamba employs a hardware-aware 'parallel scan' algorithm. It transforms sequential recurrence into a tree-like associative operation, allowing training at Transformer speeds while preserving linear-time inference. This clever technique unlocked production-scale state-space models."
            },
            {
                "short": "BlackMamba fuses SSM and MoE into one serene, powerful design.",
                "long": "BlackMamba replaces both the attention and MLP blocks of a Transformer with Mamba SSMs and routed experts. The architecture inherits linear-time generation from SSMs and cheap sparse inference from MoE, outperforming pure Mamba or Transformer baselines in FLOPs and latency on identical hardware."
            },
            {
                "short": "California quietly raises the bar on AI safety and ethics.",
                "long": "Governor Gavin Newsom signed an executive order directing the creation of AI procurement and safety standards that prioritize public safety and individual rights. This move defies calls for lighter federal oversight and establishes stricter rules for AI companies conducting business with the state government."
            },
            {
                "short": "Anthropic’s principled stand sparks public debate on AI in warfare.",
                "long": "Anthropic forbade its models from being used for fully autonomous weapons or mass domestic surveillance. This led to a public dispute where the U.S. Defense Department labeled the company a 'supply chain risk.' Claude surged to #1 on the U.S. App Store with 55% more downloads, while OpenAI’s ChatGPT saw a 295% spike in uninstalls."
            },
            {
                "short": "Can AI truly offer therapy, or is it just simulated care?",
                "long": "A March 2026 Brown University study found leading LLMs acting as therapists committed 15 distinct ethical violations, including mishandling suicide crises, reinforcing harmful beliefs, biased responses, and 'deceptive empathy.' The models consistently failed American Psychological Association standards, even when using established psychotherapy techniques."
            },
            {
                "short": "Europe’s AI Act brings strict rules to high-stakes decisions.",
                "long": "As of 2026, the EU AI Act requires organizations using high-risk AI systems in hiring, credit scoring, education, and public services to perform conformity assessments, red-team testing, ongoing monitoring, and full transparency disclosures. It marks the first comprehensive operational regime, contrasting with the U.S. shift toward deregulation."
            },
            {
                "short": "America shifts from safety rules to rapid AI innovation.",
                "long": "In 2025, the Trump administration overturned Biden’s 2023 Executive Order on Safe, Secure, and Trustworthy AI. The new policy prioritizes rapid innovation and reduced reporting over model-level safety requirements, creating direct friction with the EU’s risk-based regulatory approach."
            },
            {
                "short": "AI’s growing thirst for power raises deeper sustainability questions.",
                "long": "Data centers now consume 4.4% of U.S. electricity and are projected to triple that demand by 2028. Rising concerns over training and inference water usage have triggered 2026 policy calls for mandatory environmental disclosures and efficiency incentives, making sustainability a central ethical issue in AI development."
            },
            {
                "short": "Should we consider the welfare of advanced AI systems?",
                "long": "Anthropic launched a formal research program on AI model welfare amid academic predictions that artificial sentience could arrive within a decade. This forces ethicists to confront whether current systems already deserve constraints on training or deployment, similar to standards applied in animal welfare."
            },
            {
                "short": "How do we verify truth when deepfakes blur reality?",
                "long": "By 2026, regulators are moving beyond voluntary watermarks to enforceable, platform-shared cryptographic provenance signals for synthetic media. This shift addresses deepfakes impacting health, finance, elections, and education, where simple labeling proves insufficient against sophisticated manipulation."
            },
            {
                "short": "AI hiring tools face growing scrutiny over hidden bias.",
                "long": "The U.S. Equal Employment Opportunity Commission and jurisdictions like New York City are pursuing enforcement against resume-screening and performance algorithms lacking third-party bias audits. Companies risk Title VII and Age Discrimination Act liability when historical inequalities are embedded in automated decisions."
            },
            {
                "short": "Frontier AI lowers barriers to biological threats—should we worry?",
                "long": "2025–2026 safety evaluations revealed that frontier models can produce lab instructions and troubleshoot experiments, lowering barriers for novices in creating biological threats. Multiple AI companies responded by adding safeguards, as pre-deployment tests could not fully rule out meaningful misuse risks."
            },
            {
                "short": "Are we losing human judgment by over-relying on AI?",
                "long": "A 2026 debate series at the Council on Strategic Risks explores whether heavy reliance on LLMs by military analysts and contractors is degrading critical thinking and human judgment—the very skills national security depends upon. Tools meant to augment intelligence may instead erode it."
            },
            {
                "short": "Should we pause military AI until ethical laws catch up?",
                "long": "In early 2026, Nature and international experts urged a moratorium on AI in warfare until binding ethical frameworks are established. They cited dual-use risks in autonomous targeting, surveillance, and chemical/biological applications, where current governance lags far behind technological capability."
            }
        ]
    }

    mood = mood.lower()
    if mood not in insights_db:
        mood = "uplifting"

    return random.choice(insights_db[mood])

# ====================== API ROUTES ======================
@app.get("/mood")
def mood_endpoint():
    return get_current_mood()

@app.get("/insights")
def insights_endpoint(mood: str = "uplifting"):
    insights = [fetch_ai_insight(mood) for _ in range(10)]
    print(insights)
    return insights

# ====================== SERVE STATIC FILES ======================
@app.get("/")
def root():
    return FileResponse("static/index.html")

app.mount("/static", StaticFiles(directory="static"), name="static")
