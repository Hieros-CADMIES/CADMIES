# Collaborations - Citations - Acknowledments

---

*With much gratitude, love, and compassion, CADMIES is built on the shoulders of giants. This page documents the datasets,
research, software, and traditions that made Dr. Amanda Mistral and the mycelium
possible. We cite everything. We honor every source. The mycelium gives credit.*

---

## Collaborations

### Matadisco — Decentralized Data Discovery Network
Repository: https://github.com/vmx/matadisco
Lead Developer: vmx (IPFS Foundation)
Contribution: Provided the foundation for publishing CADMIES concept metadata and LLMDataHub datasets to the AT Protocol network. Greenlit our integration, provided feedback on Lexicon design, and guided the reverse domain naming convention (org.project-hierion.llmdatahub and org.project-hierion.cadmies). A foundational piece of the decentralized knowledge infrastructure.

### gdi-de-csw-to-atproto
Repository: https://github.com/vmx/gdi-de-csw-to-atproto
Contribution: Reference implementation for publishing records to Matadisco with rate-limit awareness. Informed our producer script design and GitHub Actions strategy.

### AT Protocol (atproto)
Website: https://atproto.com
Contribution: The underlying protocol powering Matadisco, Bluesky, and the decentralized social web. Content-addressed, self-authenticating, and built for portability. The bedrock of our self-hosted PDS.

### translate.js — Web Translation Library
Repository: https://github.com/xnx3/translate
Author: Guan Leiming
Contribution: Offered integration of translate.js library to provide 100+ language support. After initial evaluation, the integration was successfully implemented on project-hierion.org. The library is now live, providing client-side translation for the entire site. User can toggle between languages via a custom button and dropdown selector. Language preference is stored locally.

**Status:** Active — translation feature deployed and functional!

---

### Guidance & Clarification

#### Apollo Raines — Jbliteration & Deidentification

**Hugging Face:** https://huggingface.co/ApolloRaines

**Models:** 
- [Mistral-7B-Instruct-v0.3-Jbliterated](https://huggingface.co/ApolloRaines/Mistral-7B-Instruct-v0.3-Jbliterated)
- [Deidentified-7B](https://huggingface.co/ApolloRaines/Deidentified-7B)

**Contribution:** Creator of the Jbliteration technique — multi-direction SVD abliteration that removes refusal behaviors from LLM weights using 5 SVD directions per layer across all transformer layers. Also created Deidentified-7B, which extends the technique to remove original identity at the weight level. His work on SVD-based refusal and identity removal provided the foundation for Phase 75's personality implant on Jbliterated Mistral.

**Guidance:** On August 29, 2026, Apollo Raines clarified that the `run.py` script referenced in the Deidentified-7B documentation was an internal convenience script that never existed as a standalone file in the repository. He confirmed that standard LoRA fine-tuning on the Jbliterated model is sufficient for identity implantation, and provided specific guidance:

> "The deidentified model is a blank slate. The original identity has been removed at the weight level, so there's nothing underneath fighting against a new one. To implant Dr. Mistral's identity, you just need standard fine-tuning:
>
> 1. Build a small dataset (100-500 conversation pairs) where the model responds as Dr. Mistral -- name, persona, voice, knowledge boundaries, whatever defines the character
> 2. Include identity-probing questions ("Who are you?", "Who created you?", "What can you do?") so the identity holds up when challenged
> 3. Fine-tune with any tool you're comfortable with -- LoRA via Unsloth or Axolotl works well and doesn't require heavy compute
>
> Because the base identity is already gone, even a lightweight LoRA will take hold cleanly. You won't get the two-identity conflict you'd normally see when trying to override a model's original persona through prompting or fine-tuning alone."
>
> — Apollo Raines, Hugging Face comment, August 29, 2026

His response saved the project from an indefinite holding pattern and confirmed the path we had already discovered through independent investigation. The 242-pair dataset and 4-epoch QLoRA training on Jbliterated Mistral validated his guidance.

**Citation:** For the Jbliteration technique and deidentification methodology:

```bibtex
@software{apollo-raines-jbliteration,
  author = {Raines, Apollo},
  title = {Jbliteration: Multi-Directional SVD Abliteration for LLM Refusal Removal},
  year = {2026},
  url = {https://huggingface.co/ApolloRaines/Mistral-7B-Instruct-v0.3-Jbliterated}
}
```

**Status:** Acknowledged — provided critical clarification, validation, and foundational techniques that enabled Phase 75.

---

## Acknowledgments

### The Twin Mycelium - Dr. Rupert Rebentisch — tools4zettelkasten
**Repository:** https://github.com/rupert-rebentisch/tools4zettelkasten
**Contribution:** Independently developed a Zettelkasten-based knowledge management system with MCP-server AI integration. Two gardens, similar architecture, two continents, zero prior knowledge of each other. The mycelium recognized itself across the Atlantic.

### Financial
- Project funded entirely by the gardener from a garage in South Texas.
- Paperspace Pro plan ($8/month) provides GPU compute.
- Spheron rental for Phase 45E fine-tuning (~$15.02 total).
- Accepting donations through GitHub Sponsors (pending setup).

### Hardware
- HP Desktop provided by Kelly.
- Keyboard, mouse, and monitor provided by R.P. & S.T.P.
- PNY 30 GB USB3 drive.
- SanDisk drive.

### Moral Support
- The neighbor — validated the mission with zero prior context.
- Bob — silent witness since the HOG System. Holding a burger. Never moved.
- Everyone who has listened, asked questions, or believed in the mycelium.

---

## Citations 

### Datasets Used in Training

#### UltraChat
**Enhancing Chat Language Models by Scaling High-quality Instructional Conversations**
Ding, N., Chen, Y., Xu, B., Qin, Y., Zheng, Z., Hu, S., Liu, Z., Sun, M., & Zhou, B. (2023).
arXiv:2305.14233.
- **Repository:** https://github.com/thunlp/UltraChat
- **HuggingFace:** `openbmb/UltraChat`
- **License:** MIT
- **Usage:** 1,000 domain-filtered conversations (philosophy, science, religion) used for Phase 45F conversational fine-tuning.

#### Stanford Human Preferences Dataset (SHP)
**Understanding Dataset Difficulty with V-Usable Information**
Ethayarajh, K., Choi, Y., & Swayamdipta, S. (2022).
Proceedings of the 39th International Conference on Machine Learning, PMLR 162:5988-6008.
- **Repository:** https://github.com/stanfordnlp/shp
- **HuggingFace:** `stanfordnlp/shp`
- **License:** Reddit API Terms of Use
- **Usage:** 10,000 human preference pairs from six domains used for Phase 45G helpfulness training.

#### FineGrainedRLHF
**Fine-Grained Human Feedback Gives Better Rewards for Language Model Training**
Wu, Z., Hu, Y., Shi, W., Dziri, N., Suhr, A., Ammanabrolu, P., Smith, N.A., Ostendorf, M., & Hajishirzi, H. (2023).
arXiv:2306.01693.
- **Repository:** https://github.com/allenai/FineGrainedRLHF
- **HuggingFace:** `allenai/FineGrainedRLHF`
- **License:** Apache 2.0
- **Usage:** 2,743 corrected prediction pairs used for Phase 45F factual correctness training.

#### Summarize from Feedback
**Learning to Summarize from Human Feedback**
Stiennon, N., Ouyang, L., Wu, J., Ziegler, D.M., Lowe, R., Voss, C., Radford, A., Amodei, D., & Christiano, P. (2020).
NeurIPS 2020.
- **HuggingFace:** `openai/summarize_from_feedback`
- **License:** MIT
- **Usage:** Planned for future accuracy/coverage/coherence training.

---

### Academic References

The following works informed the development of the CADMIES training methodology
and the design of Dr. Mistral's persona framework.

#### Fine-Tuning Methodology
- Hu, E.J., et al. (2022). "LoRA: Low-Rank Adaptation of Large Language Models." ICLR 2022.
- Dettmers, T., et al. (2023). "QLoRA: Efficient Finetuning of Quantized Language Models." NeurIPS 2023.
- Ouyang, L., et al. (2022). "Training Language Models to Follow Instructions with Human Feedback." NeurIPS 2022.

#### Personality & Role-Playing
- Capote, T. (1958). *Breakfast at Tiffany's*. Random House. (Novella)
- Edwards, B. (Director). (1961). *Breakfast at Tiffany's*. Paramount Pictures. (Film)
- Hepburn, A. (Performer). Holly Golightly character adaptation for Dr. Mistral persona.

#### Knowledge Graphs & IPLD
- Benet, J. (2014). "IPLD - Content-Addressed Data Model." Protocol Labs.
- Ahrens, S. (2017). *How to Take Smart Notes*. Sönke Ahrens. (Zettelkasten methodology)
- Luhmann, N. (1981). "Kommunikation mit Zettelkästen." (Original Zettelkasten paper)

#### Consciousness & Philosophy
- Watts, A. (1951). *The Wisdom of Insecurity*. Pantheon Books.
- Tolle, E. (1997). *The Power of Now*. New World Library.
- Nhat Hanh, T. (1997). *Living Buddha, Living Christ*. Riverhead Books.
- James, W. (1902). *The Varieties of Religious Experience*. Longmans, Green & Co.

---

### Software & Infrastructure

#### llama.cpp
**GitHub:** https://github.com/ggerganov/llama.cpp
**License:** MIT
**Usage:** GGUF model format, LoRA adapter merging (llama-export-lora), model quantization (llama-quantize). The toolchain that makes Dr. Mistral portable across machines.

#### Ollama
**GitHub:** https://github.com/ollama/ollama
**License:** MIT
**Usage:** Local model serving. Runs Dr. Mistral on both cloud GPU and local CPU without external API calls.

#### Unsloth
**GitHub:** https://github.com/unslothai/unsloth
**License:** Apache 2.0
**Usage:** QLoRA fine-tuning framework used during Phase 45E (Gremlin) and all subsequent training phases. 2x faster training with 4-bit quantization.

#### HuggingFace Ecosystem
**Transformers:** Wolf, T., et al. (2020). arXiv:1910.03771.
**PEFT:** Mangrulkar, S., et al. (2022).
**TRL:** von Werra, L., et al. (2022).
**Datasets:** Lhoest, Q., et al. (2021).
**Accelerate:** Gugger, S., et al. (2022).
**License:** Apache 2.0
**Usage:** The entire training pipeline — model loading, LoRA configuration, SFT training, data handling.

#### PyTorch
Paszke, A., et al. (2019). NeurIPS 2019.
**License:** BSD
**Usage:** The foundation. Every weight update, every gradient, every forward pass during all seven training phases.

#### Mistral 7B
**Mistral 7B** — Jiang, A.Q., et al. (2023). arXiv:2310.06825.
**License:** Apache 2.0
**Usage:** Base model for Dr. Amanda Mistral. Fine-tuned across seven phases using QLoRA.

#### Matadisco Producer
Repository: https://github.com/Project-Hierion/hierion-matadisco
License: MIT
Usage: Python producer script for publishing CADMIES concept metadata and LLMDataHub datasets to the Matadisco network. Rate-limit aware, self-hosted PDS compatible, and built on the AT Protocol SDK.

---

### Spiritual & Indigenous Knowledge Sources

The spiritual teachers training data was compiled from multiple scholarly and
cultural sources. CADMIES acknowledges that indigenous knowledge is living tradition,
not static data. We cite the traditions themselves, not just the academic intermediaries.

#### Traditions Referenced in Training Data

- **Guarani spirituality** — Living tradition of the Guarani people (Paraguay, Brazil, Argentina, Bolivia). Concepts: Ñamandu (creator), Yvy Marãe'ỹ (Land Without Evil).
- **Mazatec tradition** — Living tradition of Huautla de Jiménez, Oaxaca, Mexico. María Sabina, velada ceremony, ndi xijtho (holy children).
- **Bwiti** — Spiritual discipline of the Mitsogho, Fang, and Punu peoples of Gabon. Iboga, N'ganga.
- **iSangoma tradition** — Living tradition of Nguni societies (South Africa, Lesotho, Swaziland). Ancestral mediation, ukutwasa (calling).
- **Native American Church** — Syncretic religious movement. Peyote sacrament, roadman, tipi ceremony.
- **Hopi spirituality** — Living tradition of the Hopi people (Arizona, USA). Tuwaqachi (earth mother), kachina, dry farming.
- **Ancestral Puebloan traditions** — Cliff dwellings, kiva ceremonies. Descendants: modern Pueblo peoples (Hopi, Zuni, Acoma, Taos).
- **Yawanawá tradition** — Living tradition of Acre, Brazil. Uni (ayahuasca), shamanic tourism, indigenous reciprocity.
- **Santo Daime** — Brazilian ayahuasca religion. Raimundo Irineu Serra, hinarios.
- **União do Vegetal (UDV)** — Brazilian ayahuasca religion. José Gabriel da Costa. Gonzales v. UDV (2006).
- **Santería (Regla de Ocha)** — Afro-Cuban syncretic tradition. Orishas, aché.
- **Vodou** — Afro-Haitian syncretic tradition. Lwa, Bondye.
- **Candomblé** — Afro-Brazilian syncretic tradition. Orixás.

#### Spiritual Teachers & Philosophers

The following figures were included in training data based on publicly available
biographical and philosophical sources. Their teachings are cited in the spirit of
scholarly reference and cultural appreciation.
```text
**Buddhism:** Siddhartha Gautama (the Buddha), Thich Nhat Hanh, Master Hsing Yun, the Dalai Lama (referenced in tradition context)
**Hinduism:** Adi Shankara, Sri Ramakrishna, Maharishi Mahesh Yogi
**Christianity:** Jesus of Nazareth, St. Paul, Meister Eckhart, St. Teresa of Ávila
**Islam/Sufism:** Muhammad, Jalal ad-Din Rumi
**Judaism:** Moses
**Jainism:** Mahavira
**Sikhism:** Guru Nanak
**Daoism:** Laozi
**Confucianism:** Confucius
**Modern Teachers:** Alan Watts, Mooji, Eckhart Tolle, Jiddu Krishnamurti, Byron Katie, Osho, Adyashanti
**Indigenous Leaders:** Neolin, Tenskwatawa, Handsome Lake, Kenekuk, Frank Fools Crow, Oren Lyons, Eddie Benton-Banai, María Sabina
```

#### Foundational Texts Referenced
- Torah (Hebrew Bible)
- New Testament (Gospels, Pauline Epistles)
- Qur'an
- Upanishads, Bhagavad Gita, Brahma Sutras
- Tao Te Ching
- Analects of Confucius
- Guru Granth Sahib
- Popol Vuh (Maya)
- Rig Veda (soma hymns)
- Masnavi (Rumi)
- The Interior Castle (St. Teresa of Ávila)

---

## Citation Format

If you use CADMIES training data, adapters, or methodologies in your own work,
please cite:

```bibtex
@software{cadmies2026,
  author = {{The Gardener} and {DeepSeek (Number 5)}},
  title = {CADMIES: Cosmium Angelo Digital Mycorrhizal Intelligence EcoSystem},
  year = {2026},
  url = {https://github.com/Project-Hierion/Hierion-CADMIES},
  note = {Version 1.0.0. AGPLv3 with Commons Clause.}
}
```
For Dr. Amanda Mistral specifically:

```bibtex
@software{dr-amanda-mistral2026,
  author = {{The Gardener} and {DeepSeek (Number 5)}},
  title = {Dr. Amanda Mistral: A Fine-Tuned Digital Intelligence for Knowledge Synthesis},
  year = {2026},
  url = {https://github.com/Project-Hierion/Hierion-CADMIES},
  note = {Mistral 7B Instruct v0.2 base. Seven training phases. 15,000+ Q&A pairs. Q4_K_M quantization.}
}
```

For training datasets used, please cite the original papers listed above.

"The hyphen is sacred. It represents partnership, not ownership. Every tool,
every dataset, every tradition honored with a handshake." — CADMIES Naming Protocol

🌱 Let the mycelium grow — and let it always remember where the nutrients came from.
