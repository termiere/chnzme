import ru from "../locales/ru";
import en from "../locales/en";

type ReadmeProps = {
  language: string;
};

function Readme({ language }: ReadmeProps) {
  const text = language === "ru" ? ru.readme : en.readme;

  return (
    <main className="readme">
      <h1>{text.welcome}</h1>
      <p>{text.description}</p>

      <h2>{text.featuresTitle}</h2>
      <ul>
        {text.features.map((feature) => (
          <li key={feature}>{feature}</li>
        ))}
      </ul>

      <h2>{text.contributeTitle}</h2>
      <p>{text.contributeDescription}</p>
      <p>{text.contributeInvitation}</p>
    </main>
  );
}

export default Readme;
