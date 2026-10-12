import "../styles/Words.css";

type WordItemProps = {
  hanzi: string;
  pinyin: string;
  translation: string;
  status: string;
  nextReview: Date | null;
  onDelete: () => void;
};

function getReviewStatus(status: string, nextReview: Date | null): string {
  if (status === "new") {
    return "NEW";
  }

  if (!nextReview || Number.isNaN(nextReview.getTime())) {
    return "LEARNING";
  }

  const diff = nextReview.getTime() - Date.now();

  if (diff <= 0) {
    return "NOW";
  }

  const minutes = Math.ceil(diff / (1000 * 60));

  if (minutes < 60) {
    return `IN ${minutes}M`;
  }

  const hours = Math.ceil(minutes / 60);

  if (hours < 24) {
    return `IN ${hours}H`;
  }

  const days = Math.ceil(hours / 24);

  return `IN ${days}D`;
}

function WordItem({
  hanzi,
  pinyin,
  translation,
  status,
  nextReview,
  onDelete,
}: WordItemProps) {
  const reviewStatus = getReviewStatus(status, nextReview);
  const isNow = reviewStatus === "NOW";

  return (
    <div className="word-card">
      <div className="word-card-top">
        <span className={`status-dot ${isNow ? "is-urgent" : ""}`} />
        <div className="word-card-actions">
          <span className={`word-badge ${isNow ? "badge-urgent" : ""}`}>
            {reviewStatus}
          </span>
          <button
            className="word-delete-btn"
            onClick={onDelete}
            aria-label="Delete word"
            title="Delete word"
          >
            ×
          </button>
        </div>
      </div>

      <div className="word-card-body">
        <span className="word-hanzi">{hanzi}</span>
      </div>

      <div className="word-card-footer">
        <span className="word-pinyin">{pinyin}</span>
        <span className="word-divider">|</span>
        <span className="word-translation">{translation}</span>
      </div>
    </div>
  );
}

export default WordItem;
