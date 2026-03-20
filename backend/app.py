from app.voice.voice_input import listen
from app.ai.text_to_sql import generate_sql
from app.db.run_query import execute_sql
from app.voice.voice_output import speak

def main():

    # Voice input
    question = listen()
    print("\nYou asked:", question)

    if "Could not" in question:
        speak("Sorry, I could not understand.")
        return

    # AI → SQL
    sql_query = generate_sql(question)
    print("\nGenerated SQL:\n", sql_query)

    results = execute_sql(sql_query)

    print("\nResults:")

    if isinstance(results, str):
        print(results)
        speak("There was an error executing the query.")
    else:
        for r in results:
            print(r)

        # Convert results to speech
        if results:
            summary = ", ".join(str(r[0]) for r in results[:5])
            speak(f"The results are {summary}")
        else:
            speak("No data found.")

if __name__ == "__main__":
    main()