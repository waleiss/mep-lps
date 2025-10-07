import { CATALOG } from "../mocks/catalog";
import type { Book } from "../types/book";


export async function listBooks(): Promise<Book[]> {
// troque por fetch real quando tiver backend
await new Promise((r) => setTimeout(r, 200));
return CATALOG;
}


export async function getBook(id: string): Promise<Book | undefined> {
await new Promise((r) => setTimeout(r, 150));
return CATALOG.find((b) => b.id === id);
}