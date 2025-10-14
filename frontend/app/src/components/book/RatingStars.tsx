export function RatingStars({ rating }: { rating: number }) {
  const full = Math.floor(rating);
  const half = rating - full >= 0.5;
  return (
    <div className="flex items-center gap-0.5" aria-label={`rating ${rating}`}>
      {Array.from({ length: 5 }).map((_, i) => (
        <span
          key={i}
          className={`text-yellow-500 ${
            i < full
              ? "opacity-100"
              : i === full && half
              ? "opacity-70"
              : "opacity-30"
          }`}
        >
          ★
        </span>
      ))}
      <span className="ml-2 text-xs text-slate-500">{rating.toFixed(1)}</span>
    </div>
  );
}
