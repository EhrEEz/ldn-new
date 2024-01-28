export interface VehicleSmall {
	id?: number;
	creation_date?: string;
	seats?: string;
	color_code?: string;
	color_name?: string;
	model_manufacturer?: string;
	model_name?: string;
	vehicle_image?: string;
	vehicle_daily_price: string;
	vehicle_location?: string;
	vehicle_city?: string;
	transmission?: string;
	mileage?: number;
	fuel_type?: string;
	slug?: string;
	location_area?: boolean;
	reg_no: string;
}
export interface MainVehicle {
	id?: number;
	creation_date?: string;
	modification_date?: string;
	name?: string;
	reg_no: string;
	on_trip?: boolean;
	seats?: number;
	color_name?: string;
	color_code?: string;
	model_name?: string;
	model_manufacturer?: string;
	is_active?: boolean;
	slug?: string;
	vehicle_image?: string;
	vehicle_daily_price: number;
	location_area?: true;
	vehicle_location?: string;
	transmission?: string;
	fuel_type?: string;
	mileage?: number;
	vehicle_owner: {
		id: string;
		full_name: string;
	};
	vehicle_name?: string;
	vehicle_city?: number;
}
