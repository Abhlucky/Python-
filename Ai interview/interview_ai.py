from openai import OpenAI
import os
import json
import re
import tempfile
import sys

# ---------------- API KEY CHECK ----------------
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    print("❌ ERROR: OPENAI_API_KEY set nahi hai!")
    print("Terminal mein ye chalao (apni key daal ke):")
    print('   export OPENAI_API_KEY="sk-xxxxxx"      (Mac/Linux)')
    print('   setx OPENAI_API_KEY "sk-xxxxxx"         (Windows, phir naya terminal kholo)')
    sys.exit(1)

client = OpenAI(api_key=API_KEY)
MODEL = "gpt-4o-mini"

# Voice support check
VOICE_AVAILABLE = True
try:
    import speech_recognition as sr
except ImportError:
    VOICE_AVAILABLE = False


def generate_question(role, level, history):
    past = "\n".join(f"- {h['q']}" for h in history) or "None"
    prompt = f"""You are an interviewer for role: {role}, level: {level}.
Already asked:
{past}

Ask ONE new interview question. Only the question, nothing else."""
    try:
        res = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )
        return res.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Question generate karte waqt error: {e}")
        return "Tell me about yourself."  # fallback question


def evaluate_answer(role, question, answer):
    prompt = f"""Role: {role}
Question: {question}
Answer: {answer}

Give feedback as STRICT JSON only:
{{
 "communication": 1-10,
 "relevance": 1-10,
 "confidence": 1-10,
 "overall_score": 1-10,
 "feedback": "short constructive feedback"
}}"""
    try:
        res = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        text = res.choices[0].message.content.strip()
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            text = match.group(0)
        return json.loads(text)
    except Exception as e:
        print(f"⚠️ Evaluation error: {e}")
        return {"communication": 5, "relevance": 5, "confidence": 5,
                "overall_score": 5, "feedback": "Evaluation fail hui, default score diya gaya."}


def record_voice_answer():
    if not VOICE_AVAILABLE:
        print("⚠️ Voice feature available nahi hai (speech_recognition/pyaudio missing).")
        return None

    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("🎙️ Bolna shuru karo... (5 sec silence pe khud ruk jayega)")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=60)
            print("⏳ Processing voice...")

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio.get_wav_data())
            tmp_path = tmp.name

        with open(tmp_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )
        os.remove(tmp_path)
        return transcript.text.strip()

    except sr.WaitTimeoutError:
        print("⚠️ Kuch bola nahi gaya (timeout). Type kar do.")
        return None
    except OSError:
        print("⚠️ Mic detect nahi hua. Type kar do.")
        return None
    except Exception as e:
        print(f"⚠️ Voice error: {e}. Type kar do.")
        return None


def get_answer():
    choice = input("Answer kaise doge? (v = voice / t = type): ").strip().lower()

    if choice == "v":
        result = record_voice_answer()
        if result:
            print(f"📝 Tumne bola: \"{result}\"")
            confirm = input("Ye sahi hai? (y = yes, n = phir se type karo): ").strip().lower()
            if confirm == "y":
                return result
            else:
                return input("✍️ Apna answer type karo: ").strip()
        else:
            return input("✍️ Apna answer type karo: ").strip()
    else:
        return input("✍️ Apna answer type karo: ").strip()


def main():
    print("=== 🎤 AI Interview Assistant ===\n")
    if not VOICE_AVAILABLE:
        print("(Note: Voice input disabled - packages missing. Sirf typing chalegi.)\n")

    role = input("Job Role (e.g. Software Engineer): ").strip()
    level = input("Level (Fresher/Mid/Senior): ").strip()

    try:
        num_q = int(input("Kitne questions chahiye? (e.g. 3): ").strip())
    except ValueError:
        num_q = 3
        print("Invalid input, default 3 questions rakhe ja rahe hain.")

    history = []

    for i in range(num_q):
        print(f"\n--- Question {i+1} ---")
        question = generate_question(role, level, history)
        print(f"🤖 AI: {question}\n")

        answer = get_answer()

        if not answer:
            print("⚠️ Khali answer, skip kar rahe hain.")
            continue

        print("\n⏳ Evaluating...")
        feedback = evaluate_answer(role, question, answer)

        print(f"\n📊 Communication: {feedback['communication']}/10")
        print(f"📊 Relevance:     {feedback['relevance']}/10")
        print(f"📊 Confidence:    {feedback['confidence']}/10")
        print(f"📊 Overall:       {feedback['overall_score']}/10")
        print(f"💡 Feedback: {feedback['feedback']}")

        history.append({"q": question, "a": answer, "fb": feedback})

    if history:
        print("\n\n========== 🏆 FINAL REPORT ==========")
        total = {"communication": 0, "relevance": 0, "confidence": 0, "overall_score": 0}
        for h in history:
            for k in total:
                total[k] += h["fb"][k]
        n = len(history)
        for k, v in total.items():
            print(f"{k.capitalize()}: {v/n:.1f}/10")
    else:
        print("\nKoi answer submit nahi hua.")


if __name__ == "__main__":
    main()