export type Book = {
categories?: string[];
coverUrl: string | undefined;
id: string;
title: string;
author: string;
price: number;
rating: number;
cover: string;
tagline?: string;
description?: string;
};


export type CartItem = { book: Book; qty: number };