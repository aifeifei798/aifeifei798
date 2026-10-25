<div align="center">

# Hi, I'm aifeifei798 👋

**I work on the unglamorous half of AI — making big models actually fit on small GPUs.**

Sparse MoE architectures, from-scratch model reproductions, and the local tooling that surrounds them.
Most of it runs on a single consumer card. All of it is public.

[![Website](https://img.shields.io/badge/feimatrix.com-111111?style=flat-square&logo=firefox&logoColor=white)](https://feimatrix.com/)
[![PyPI harmonic-llm](https://img.shields.io/pypi/v/harmonic-llm?style=flat-square&label=harmonic-llm&color=blue)](https://pypi.org/project/harmonic-llm/)
[![PyPI flashcodec-kv](https://img.shields.io/pypi/v/flashcodec-kv?style=flat-square&label=flashcodec-kv&color=blue)](https://pypi.org/project/flashcodec-kv/)
[![Followers](https://img.shields.io/github/followers/aifeifei798?style=flat-square&color=black)](https://github.com/aifeifei798?tab=followers)

</div>

---

## 🧭 What I'm after

Frontier capability is increasingly a memory problem, not a compute problem. My work attacks it from three directions:

| Direction | The question I keep asking |
| :--- | :--- |
| **Heterogeneous sparsity** | Can a sub-billion active-parameter model hold 7B-class breadth if experts live in host RAM and stream in on demand? |
| **Signal processing on tensors** | If a KV cache is really a high-dimensional image, what do JPEG and PNG already know that LLM serving doesn't? |
| **Removing the cluster** | What does a fine-tuning / inference stack look like when the only machine available is the one on your desk? |

Every repo below is an attempt at one of those, built end-to-end: kernels and training loops on one side, a usable web UI on the other.

---

## 🔬 Selected work

### Sparse MoE on consumer hardware

| Project | What it is |
| :--- | :--- |
| **[Myriad-MoE-25K-Micro-Experts](https://github.com/aifeifei798/Myriad-MoE-25K-Micro-Experts)** | Dual VRAM dense cores + 25,200 micro-experts streamed from 1.54 GB host RAM with ~40 ms live hot-swap. 0.9B active parameters, 7B+ baseline behaviour. Proposed upstream in [transformers#49183](https://github.com/huggingface/transformers/issues/49183). |
| **[BigLittle-MoE](https://github.com/aifeifei798/BigLittle-MoE)** / **[DualBigLittle-MoE](https://github.com/aifeifei798/DualBigLittle-MoE)** | The hierarchical big-core / micro-expert split that Myriad grew out of — one core per cognitive domain, sparsity only where it pays. |
| **[Heretic-Scalpel-TriTier-E2B](https://github.com/aifeifei798/Heretic-Scalpel-TriTier-E2B)** | Tri-Tier Swarm Mixture-of-Adapters on a Gemma 4 (E2B) backbone — three adapters, three roles, one frozen trunk. |
| **[Heretic-Scalpel-Swarm-Forge](https://github.com/aifeifei798/Heretic-Scalpel-Swarm-Forge)** | The training side of the series: `forge_core` (pure-ML library) + FastAPI backend + React console. |
| **[myriad-moe-console](https://github.com/aifeifei798/myriad-moe-console)** | Web client for the 25K-expert model: streaming chat, collapsible reasoning traces, and a live view of which experts fired. |

### Architecture reproduction, from scratch

| Project | What it is |
| :--- | :--- |
| **[DeepSeek-Pro-Mini](https://github.com/aifeifei798/DeepSeek-Pro-Mini)** | A from-zero reimplementation of the DeepSeek-V3/V4 core — MLA latent attention, 8-expert sparse MoE, SqrtSoftplus gating, bounded SwiGLU. 153M total / 60M active, **52k+ tok/s** on one GPU, 245M-token pretrain + 900k SFT turns, with a real-time MoE gate heatmap in the terminal. |
| **[Mini-Architecture](https://github.com/aifeifei798/Mini-Architecture)** | Small reference implementations of the pieces I keep re-deriving. |

### Inference efficiency & interpretability

| Project | What it is |
| :--- | :--- |
| **[flashcodec-kv](https://github.com/aifeifei798/flashcodec-kv)** | Treats the sequence axis of a `(B,H,S,D)` KV cache as an image: JPEG-style block DCT in the frequency domain, PNG-style anchor + delta coding in the time domain. Drop-in `transformers` 5.x `Cache` backend. |
| **[Harmonic-LLM](https://github.com/aifeifei798/Harmonic-LLM)** | Training-free amplitude outlier suppression for `q_proj` / `o_proj`: crest-factor sidechain detection plus 8-band DCT wave-shaping, one forward hook, no weights touched. On PyPI. |

### Training & applied ML services

| Project | What it is |
| :--- | :--- |
| **[unsloth-gui](https://github.com/aifeifei798/unsloth-gui)** | Browser workbench for single-GPU Unsloth fine-tuning: data mapping, resumable LoRA SFT, live TensorBoard, streaming chat test. Bilingual EN/ZH, 8 GB VRAM to start. |
| **[humanizer](https://github.com/aifeifei798/humanizer)** | Local 12B rewrite service that turns AI drafts into human prose — streaming output, 21 writing personas, rewrite-span highlighting. |
| **[Timestral](https://github.com/aifeifei798/Timestral)** / **[timesfm](https://github.com/aifeifei798/timesfm)** | Zero-shot probabilistic forecasting APIs: univariate/multivariate, missing values, covariates, 21 quantiles, with a Chart.js console. |
| **[finaudit-ai](https://github.com/aifeifei798/finaudit-ai)** / **[finaudit-ai-fast](https://github.com/aifeifei798/finaudit-ai-fast)** | Multi-agent financial audit and fraud screening with audit-grade guardrails; the `-fast` variant does the deterministic math in tools instead of tokens. |
| **[AI-Website-Generator](https://github.com/aifeifei798/AI-Website-Generator)** | One prompt in, a complete multi-section website out (Gemini + Jinja2). |

### Creative, audio & video tooling

| Project | What it is |
| :--- | :--- |
| **[ComfyUI-FeiFei](https://github.com/aifeifei798/ComfyUI-FeiFei)** | ComfyUI node pack: LLM prompt director, prompt enhancing, captioning, aspect-ratio sizing, style/character templates, film grain and tone grading, subtitle cropping. |
| **[global-style-photobook-studio](https://github.com/aifeifei798/global-style-photobook-studio)** | Six-style photobook prompt generator (HK / JP / KR / NY / CA / swimwear), 400+ presets, 92 curated sets. |
| **[Beautiful-Singing-Voice-VST3](https://github.com/aifeifei798/Beautiful-Singing-Voice-VST3)** | PyQt6 tool that fixes AI-generated vocals: Demucs stem split, fixed DSP chain, A/B monitoring. |
| **[music_studio](https://github.com/aifeifei798/music_studio)** | Desktop song workstation on YuE2-3B — lyrics in, 48 kHz stereo track with vocals out. |
| **[FastMusic](https://github.com/aifeifei798/FastMusic)** | Local music/MTV streaming player: React SPA + Express, HTTP-Range playback, `.mkv` remux, 10-band EQ and spectrum view. |
| **[stereo_eq](https://github.com/aifeifei798/stereo_eq)** | Real-time PipeWire system-output and mic-monitor EQ for Linux, 60 presets. |

### Developer tooling

| Project | What it is |
| :--- | :--- |
| **[opencode-monitor](https://github.com/aifeifei798/opencode-monitor)** | Read-only dashboard that draws an OpenCode run as a live graph and tells you *why* it is stuck. |
| **[context-mode-opencode-v2](https://github.com/aifeifei798/context-mode-opencode-v2)** | Context-mode wrapped as an OpenCode v2 plugin. |
| **[feicms](https://github.com/aifeifei798/feicms)** | Multi-source resource aggregation: collectors → DB → FastAPI → DaisyUI admin panel. |

I also run patched forks of **llama.cpp**, **transformers**, and **opencode** whenever the upstream is the thing standing in the way — a fair share of the commits in my graph are there.

---

## 🛠️ Stack

**Modelling** PyTorch · CUDA · Triton · Hugging Face Transformers · Unsloth · bitsandbytes
**Serving** FastAPI · Uvicorn · SSE streaming · vLLM-style batching · host-pinned expert paging
**Interfaces** React + Vite · Tailwind · Jinja2 · PyQt6 · ComfyUI nodes · JUCE/VST3
**Audio/DSP** Demucs · PipeWire · ffmpeg · DCT / EQ / spectrogram work
**Everyday** Python · TypeScript · Linux (Mint/Debian) · systemd · Docker · uv

---

## 📊 GitHub

<div align="center">

<img height="150" src="https://github-readme-stats.vercel.app/api?username=aifeifei798&show_icons=true&hide_title=true&hide_border=true&theme=github_dark" alt="GitHub stats" />
<img height="150" src="https://github-readme-stats.vercel.app/api/top-langs/?username=aifeifei798&layout=compact&hide_border=true&theme=github_dark&langs_count=8" alt="Top languages" />

</div>

---

<div align="center">

**Currently:** squeezing more experts into less RAM, and teaching a 60M-active model to write like it isn't one.
Issues and PRs are the best way to reach me — I read everything.

</div>
