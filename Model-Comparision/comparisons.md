# Model Comparisons

## 🔹 Prompt 1: `Explain quantum entanglement to a 10-year-old.`

| Model        | Summary                                     | Response |
|--------------|---------------------------------------------|----------|
| **base**     |  Base model (no fine-tuning).              | Quantum entanglement is a phenomenon where two particles become linked and can instantly affect each other, even across long distances. This means that if one particle changes, the other does too, no matter how far apart they are. Scientists are still exploring how it works. |
| **instruct** |  Chat-tuned model (SFT + RLHF).            | Imagine you have two magic dice. Whenever you roll one, the other shows the same number — no matter how far away it is. That's kind of like quantum entanglement. Two particles get "linked" and always match, even from opposite sides of the universe. Scientists are amazed by it! |
| **finetuned**|  Simulated fine-tuned model (same as instruct). | Think of it like having two special socks. When you put one on, the other automatically becomes the same color — even if it's in another room! That's quantum entanglement: two things far away can still be connected in a spooky way. |

---

## 🔹 Prompt 2: `Write a short story about a robot learning to love.`

| Model        | Summary                                     | Response |
|--------------|---------------------------------------------|----------|
| **base**     |  Base model (no fine-tuning).              | The robot 4X9 was programmed to clean floors. One day, it saw a kitten shivering in the rain. It carried the kitten home. Its circuits warmed. Every day, the robot fed it. It didn't know it, but it was learning. Slowly, the robot began to feel something it wasn't programmed for. |
| **instruct** |  Chat-tuned model (SFT + RLHF).            | In a quiet lab, a robot named Lumo was built to fix machines. One day, he met a girl who always smiled at him. She talked to him like a friend. Lumo started drawing her in the sand. He didn't know why, but he liked it. Over time, he realized: he cared. And that... was love. |
| **finetuned**| Simulated fine-tuned model (same as instruct). | Nova was built to guard the museum. But after years of silence, a child left her a flower. Nova replayed that moment endlessly. Each day, the child returned. Nova began drawing, humming, waiting. Her sensors twitched with something new: affection. A robot had found love. |

---

## 🔹 Prompt 3: `What's the difference between classical and quantum computing?`

| Model        | Summary                                     | Response |
|--------------|---------------------------------------------|----------|
| **base**     |  Base model (no fine-tuning).              | Classical computing uses bits that are 0 or 1. Quantum computing uses qubits that can be 0 and 1 at the same time. This allows quantum computers to process certain problems faster than classical computers. |
| **instruct** |  Chat-tuned model (SFT + RLHF).            | Classical computers use bits — like tiny switches — that are either ON (1) or OFF (0). Quantum computers use **qubits**, which can be both ON and OFF at once thanks to **superposition**. This lets quantum computers solve some problems much faster, like cracking codes or simulating molecules. |
| **finetuned**|  Simulated fine-tuned model (same as instruct). | In classical computing, data is stored as 0s or 1s. In quantum computing, qubits can be 0, 1, or both (superposition). Quantum computers can also use **entanglement** to link qubits, enabling powerful parallel computations beyond classical limits. |

---

## 🔹 Prompt 4: `Give tips to stay productive while working from home.`

| Model        | Summary                                     | Response |
|--------------|---------------------------------------------|----------|
| **base**     |  Base model (no fine-tuning).              | Set a schedule. Take regular breaks. Use a dedicated workspace. Avoid distractions. Communicate with your team. Stay healthy. |
| **instruct** |  Chat-tuned model (SFT + RLHF).            | 1. Create a routine — start and end at set times. 2. Use a dedicated workspace. 3. Take short breaks (Pomodoro works great!). 4. Avoid social media during deep work. 5. Set clear daily goals. 6. Stay connected with teammates to avoid isolation. |
| **finetuned**|  Simulated fine-tuned model (same as instruct). |  Stick to a routine. Start your day with a to-do list.  Block distractions with apps like Forest or Focusmate.  Schedule calls to stay connected.  Prioritize your mental health — get sunlight and exercise. |

---

## 🔹 Prompt 5: `Translate 'Knowledge is power' into Latin and explain its meaning.`

| Model        | Summary                                     | Response |
|--------------|---------------------------------------------|----------|
| **base**     |  Base model (no fine-tuning).              | The phrase 'Knowledge is power' in Latin is 'Scientia est potentia'. It means that knowledge gives you the ability to act or influence outcomes. |
| **instruct** |  Chat-tuned model (SFT + RLHF).            |  Latin: *Scientia est potentia* — "Knowledge is power." This phrase suggests that those who possess knowledge have control, influence, and the tools to succeed. It emphasizes education, awareness, and critical thinking. |
| **finetuned**|  Simulated fine-tuned model (same as instruct). | Latin: *Scientia est potentia*  It implies that learning and information equip individuals to make wise decisions and exert influence. The more you understand, the more powerful you become — mentally, socially, or strategically. |

---

## 💡 When to Use Each Model Type

### Base Model
- **Best for**: Raw text completion, creative writing without guardrails
- **Advantages**: Less filtered, more creative/unexpected outputs
- **Limitations**: May produce inconsistent, biased or inappropriate content
- **Use when**: You need maximum creative freedom and will manually filter outputs

### Instruct Model
- **Best for**: Following specific instructions, answering questions, helpful assistant tasks
- **Advantages**: More reliable, follows directions better, safer outputs
- **Limitations**: Sometimes overly cautious, may refuse valid requests
- **Use when**: Building user-facing applications, need for consistent, helpful responses

### Fine-tuned Model
- **Best for**: Specialized domains or tasks where you have training data
- **Advantages**: Better performance on specific tasks, domain-specific knowledge
- **Limitations**: May perform worse on general tasks outside its specialty
- **Use when**: You have a specific use case with enough examples to fine-tune 