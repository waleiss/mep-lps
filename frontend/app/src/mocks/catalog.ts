import type { Book } from "../types/book";


export const CATALOG: Book[] = [
	{
		id: "prag-prog",
		title: "The Pragmatic Programmer",
		author: "Hunt & Thomas",
		price: 119,
		rating: 4.9,
		cover: "https://images.unsplash.com/photo-1528207776546-365bb710ee93?w=640&q=80&auto=format",
		coverUrl: "https://images.unsplash.com/photo-1528207776546-365bb710ee93?w=640&q=80&auto=format",
	},
	{
		id: "clean-arch",
		title: "Clean Architecture",
		author: "Robert C. Martin",
		price: 129.9,
		rating: 4.8,
		cover: "https://images.unsplash.com/photo-1524578271613-d550eacf6090?w=640&q=80&auto=format",
		coverUrl: "https://images.unsplash.com/photo-1524578271613-d550eacf6090?w=640&q=80&auto=format",
	},
	{
		id: "js-good",
		title: "JavaScript: The Good Parts",
		author: "Douglas Crockford",
		price: 89,
		rating: 4.4,
		cover: "https://images.unsplash.com/photo-1513475382585-d06e58bcb0ea?w=640&q=80&auto=format",
		coverUrl: "https://images.unsplash.com/photo-1513475382585-d06e58bcb0ea?w=640&q=80&auto=format",
	},
];