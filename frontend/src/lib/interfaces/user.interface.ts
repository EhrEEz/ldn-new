import type { CustomError } from '$lib/interfaces/error.interface';

export interface Token {
	refresh?: string;
	access?: string;
}
export interface User {
	id?: string;
	email?: string;
	phone_number?: string;
	password?: string;
	tokens?: Token;
	bio?: string;
	full_name?: string;
	birth_date?: string;
	is_staff?: boolean;
	error?: Array<CustomError>;
}

export interface UserResponse {
	user?: User;
}
