export interface Application {
	name: string;
	skills: string[];
	email: string;
	position?: string;
}

export interface AIProvider {
	name: string;
	icon: string;
}

export interface FilterKeyword {
	category: string;
	value: string;
}
