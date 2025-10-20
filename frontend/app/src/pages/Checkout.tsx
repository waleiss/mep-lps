import { useState, useMemo } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useCart } from "../context/CartContext";

type Address = {
  name: string;
  zip: string;
  street: string;
  number: string;
  complement?: string;
  city: string;
  state: string;
};

type PaymentMethod = "card" | "pix" | "boleto";

type CardData = {
  holder: string;
  number: string;
  exp: string; // MM/AA
  cvv: string;
};

const money = (v: number) =>
  v.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

export default function Checkout() {
  const nav = useNavigate();
  const { user } = useAuth();
  const { items, subtotal, shipping, total, clear } = useCart();

  // ------------------ estado do formulário ------------------
  const [address, setAddress] = useState<Address>({
    name: user?.name ?? "",
    zip: "",
    street: "",
    number: "",
    complement: "",
    city: "",
    state: "",
  });

  const [payMethod, setPayMethod] = useState<PaymentMethod>("card");
  const [card, setCard] = useState<CardData>({
    holder: "",
    number: "",
    exp: "",
    cvv: "",
  });

  // ------------------ validações simples ------------------
  const perfilIncompleto = !user || !user.email || !user.name;

  const addressValid = useMemo(() => {
    const { name, zip, street, number, city, state } = address;
    return [name, zip, street, number, city, state].every(
      (v) => v && v.trim().length > 0
    );
  }, [address]);

  const paymentValid = useMemo(() => {
    if (payMethod === "pix" || payMethod === "boleto") return true;
    // cartão bem simples (não é validação de verdade)
    return (
      card.holder.trim().length > 4 &&
      /^\d{13,19}$/.test(card.number.replace(/\s/g, "")) &&
      /^\d{2}\/\d{2}$/.test(card.exp) &&
      /^\d{3,4}$/.test(card.cvv)
    );
  }, [payMethod, card]);

  const canFinish =
    !!user &&
    items.length > 0 &&
    !perfilIncompleto &&
    addressValid &&
    paymentValid;

  // ------------------ finalizar (mock) ------------------
  const finishOrder = () => {
    if (!canFinish) return;

    // Aqui você chamaria o gateway:
    // await ordersApi.create({
    //   items, address, payment: { method: payMethod, card },
    //   total, subtotal, shipping
    // });

    clear();
    nav("/account"); // "Meus pedidos"
  };

  if (items.length === 0) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <h1 className="text-2xl font-bold mb-2">Seu carrinho está vazio</h1>
        <Link to="/" className="text-indigo-700 underline">
          Voltar à loja
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto p-6 grid md:grid-cols-3 gap-8">
      {/* Coluna esquerda: Itens + Formulários */}
      <div className="md:col-span-2 space-y-8">
        <h1 className="text-2xl font-bold text-indigo-900">Finalizar compra</h1>

        {!user && (
          <div className="p-4 border rounded-lg bg-yellow-50 text-sm">
            Você precisa{" "}
            <Link to="/login" className="text-indigo-700 underline">
              entrar
            </Link>{" "}
            para finalizar.
          </div>
        )}

        {user && perfilIncompleto && (
          <div className="p-4 border rounded-lg bg-yellow-50 text-sm">
            Complete seus dados em{" "}
            <Link to="/account/profile" className="text-indigo-700 underline">
              Minha conta
            </Link>
            .
          </div>
        )}

        {/* Itens do carrinho */}
        <ul className="divide-y rounded-xl border bg-white">
          {items.map((it) => (
            <li key={it.book.id} className="p-4 flex gap-4">
              <img
                src={it.book.cover}
                className="w-16 h-16 rounded-lg object-cover"
              />
              <div className="flex-1">
                <div className="font-semibold">{it.book.title}</div>
                <div className="text-sm text-slate-600">{it.book.author}</div>
              </div>
              <div className="text-sm">x{it.qty}</div>
              <div className="font-semibold">
                {money(it.book.price * it.qty)}
              </div>
            </li>
          ))}
        </ul>

        {/* Endereço de entrega */}
        <section className="rounded-xl border p-4 bg-white">
          <h2 className="font-semibold mb-3">Endereço de entrega</h2>
          <div className="grid sm:grid-cols-2 gap-3">
            <Input
              label="Nome completo"
              value={address.name}
              onChange={(v) => setAddress((a) => ({ ...a, name: v }))}
            />
            <Input
              label="CEP"
              placeholder="00000-000"
              value={address.zip}
              onChange={(v) => setAddress((a) => ({ ...a, zip: v }))}
            />
            <Input
              label="Rua"
              value={address.street}
              onChange={(v) => setAddress((a) => ({ ...a, street: v }))}
            />
            <Input
              label="Número"
              value={address.number}
              onChange={(v) => setAddress((a) => ({ ...a, number: v }))}
            />
            <Input
              label="Complemento (opcional)"
              value={address.complement ?? ""}
              onChange={(v) => setAddress((a) => ({ ...a, complement: v }))}
            />
            <Input
              label="Cidade"
              value={address.city}
              onChange={(v) => setAddress((a) => ({ ...a, city: v }))}
            />
            <Input
              label="Estado"
              value={address.state}
              onChange={(v) => setAddress((a) => ({ ...a, state: v }))}
            />
          </div>
          {!addressValid && (
            <p className="text-xs text-red-600 mt-2">
              Preencha todos os campos obrigatórios.
            </p>
          )}
        </section>

        {/* Pagamento */}
        <section className="rounded-xl border p-4 bg-white">
          <h2 className="font-semibold mb-3">Pagamento</h2>

          <div className="flex gap-3 mb-4">
            <Toggle
              value={payMethod}
              thisValue="card"
              onChange={setPayMethod}
              label="Cartão"
            />
            <Toggle
              value={payMethod}
              thisValue="pix"
              onChange={setPayMethod}
              label="PIX"
            />
            <Toggle
              value={payMethod}
              thisValue="boleto"
              onChange={setPayMethod}
              label="Boleto"
            />
          </div>

          {payMethod === "card" && (
            <div className="grid sm:grid-cols-2 gap-3">
              <Input
                label="Nome impresso no cartão"
                value={card.holder}
                onChange={(v) => setCard((c) => ({ ...c, holder: v }))}
              />
              <Input
                label="Número"
                placeholder="0000 0000 0000 0000"
                value={card.number}
                onChange={(v) => setCard((c) => ({ ...c, number: v }))}
              />
              <Input
                label="Validade (MM/AA)"
                placeholder="MM/AA"
                value={card.exp}
                onChange={(v) => setCard((c) => ({ ...c, exp: v }))}
              />
              <Input
                label="CVV"
                placeholder="000"
                value={card.cvv}
                onChange={(v) => setCard((c) => ({ ...c, cvv: v }))}
              />
            </div>
          )}

          {payMethod === "pix" && (
            <p className="text-sm text-slate-600">
              O QR Code será exibido após confirmar o pedido (mock).
            </p>
          )}

          {payMethod === "boleto" && (
            <p className="text-sm text-slate-600">
              O boleto será gerado após confirmar o pedido (mock).
            </p>
          )}

          {!paymentValid && (
            <p className="text-xs text-red-600 mt-2">
              Preencha os dados de pagamento corretamente.
            </p>
          )}
        </section>
      </div>

      {/* Coluna direita: Resumo */}
      <aside className="h-fit rounded-xl border p-4 bg-white">
        <h2 className="font-semibold mb-3">Resumo</h2>
        <div className="flex justify-between text-sm mb-1">
          <span>Subtotal</span>
          <span>{money(subtotal)}</span>
        </div>
        <div className="flex justify-between text-sm mb-3">
          <span>Frete</span>
          <span>{money(shipping)}</span>
        </div>
        <hr />
        <div className="flex justify-between font-semibold text-lg mt-3">
          <span>Total</span>
          <span>{money(total)}</span>
        </div>

        <button
          disabled={!canFinish}
          onClick={finishOrder}
          className={`w-full mt-4 rounded-lg py-2.5 ${
            canFinish
              ? "bg-indigo-700 text-white hover:bg-indigo-800"
              : "bg-slate-200 text-slate-500 cursor-not-allowed"
          }`}
        >
          Finalizar compra
        </button>

        <p className="text-xs text-slate-500 mt-2">
          Ao finalizar, você concorda com nossos termos e condições.
        </p>
      </aside>
    </div>
  );
}

/* ------------------ pequenos componentes UI ------------------ */
function Input({
  label,
  value,
  onChange,
  placeholder,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  placeholder?: string;
}) {
  return (
    <label className="text-sm">
      <span className="block text-slate-600 mb-1">{label}</span>
      <input
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-indigo-400 outline-none"
      />
    </label>
  );
}

function Toggle({
  value,
  thisValue,
  onChange,
  label,
}: {
  value: PaymentMethod;
  thisValue: PaymentMethod;
  onChange: (v: PaymentMethod) => void;
  label: string;
}) {
  const active = value === thisValue;
  return (
    <button
      type="button"
      onClick={() => onChange(thisValue)}
      className={`px-3 py-1.5 rounded-full border ${
        active
          ? "border-indigo-600 text-indigo-700 bg-indigo-50"
          : "border-slate-200"
      }`}
    >
      {label}
    </button>
  );
}
