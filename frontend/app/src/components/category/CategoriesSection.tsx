import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import type { Category } from "../../mocks/categories";

type Props = {
  title?: string;
  categories: Category[];
};

const ArrowBtn = ({
  onClick,
  dir,
}: {
  onClick: () => void;
  dir: "left" | "right";
}) => (
  <button
    onClick={onClick}
    aria-label={dir === "left" ? "Anterior" : "Próximo"}
    className="size-10 grid place-items-center rounded-full border border-slate-200 bg-white/90 backdrop-blur hover:shadow-sm active:scale-95 transition"
  >
    {dir === "left" ? "←" : "→"}
  </button>
);

const CategoryCard = ({ c }: { c: Category }) => (
  <Link
    to={`/category/${c.slug}`}
    className="block rounded-2xl border border-slate-200 bg-white overflow-hidden hover:shadow-md transition"
  >
    <div className="aspect-[16/10] w-full overflow-hidden">
      <img
        src={c.image}
        alt={c.name}
        className="w-full h-full object-cover"
        loading="lazy"
      />
    </div>
    <div className="p-3 text-center">
      <div className="font-medium text-indigo-900">{c.name}</div>
    </div>
  </Link>
);

export default function CategoriesSection({
  title = "Explore as categorias mais procuradas",
  categories,
}: Props) {
  const [start, setStart] = useState(0);
  const pageSize = 3;

  const page = useMemo(() => {
    if (!categories.length) return [];
    const wrap = (i: number) => (i + categories.length) % categories.length;
    return Array.from({ length: Math.min(pageSize, categories.length) }).map(
      (_, idx) => categories[wrap(start + idx)]
    );
  }, [start, categories]);

  return (
    <section className="relative max-w-6xl mx-auto px-4 py-10">
      {/* faixa suave no topo */}
      <div className="pointer-events-none absolute inset-x-0 -top-6 h-10 bg-gradient-to-r from-rose-100 via-indigo-100 to-emerald-100 opacity-60 rounded-full blur-2xl" />

      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl md:text-3xl font-bold text-indigo-900">
          {title}
        </h2>
        <div className="flex gap-2">
          <ArrowBtn
            dir="left"
            onClick={() =>
              setStart((s) => (s - 1 + categories.length) % categories.length)
            }
          />
          <ArrowBtn
            dir="right"
            onClick={() => setStart((s) => (s + 1) % categories.length)}
          />
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {page.map((c) => (
          <CategoryCard key={c.id} c={c} />
        ))}
      </div>

      <div className="mt-8 flex justify-center">
        <Link
          to="/categories"
          className="inline-flex items-center gap-2 rounded-full border border-indigo-200 px-6 py-2 text-indigo-900 hover:bg-indigo-50 active:scale-95 transition"
        >
          VEJA MAIS <span>→</span>
        </Link>
      </div>
    </section>
  );
}
