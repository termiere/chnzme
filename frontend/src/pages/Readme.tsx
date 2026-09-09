import ru from "../locales/ru";
import en from "../locales/en";

type ReadmeProps = {
  language: string;
};

function Readme({ language }: ReadmeProps) {
  const text = language === "ru" ? ru.readme : en.readme;

  return (
    <main className="readme">
      <h1># {text.welcome}</h1>

      <p>{text.description}</p>

      <p>{text.materials}</p>

      <h1># {text.whatIs}</h1>

      <p>{text.idea}</p>

      <p>{text.canDo}</p>

      <ul>
        <li>{text.learnWords}</li>
        <li>{text.learnPinyin}</li>
        <li>{text.learnGrammar}</li>
        <li>{text.learnHsk}</li>
        <li>{text.review}</li>
        <li>{text.progress}</li>
      </ul>

      <h1># {text.guide}</h1>

      <p>{text.guideDescription}</p>

      <p>
        <strong>Words</strong> — {text.words}
      </p>

      <p>
        <strong>Grammar</strong> — {text.grammar}
      </p>

      <p>
        <strong>Profile</strong> — {text.profile}
      </p>

      <h1># {text.goal}</h1>

      <p>{text.goalDescription}</p>

      <p>{text.goalDescription2}</p>

      <h1># {text.startLearning}</h1>

      <p>{text.startDescription}</p>
    </main>
  );
}

export default Readme;
