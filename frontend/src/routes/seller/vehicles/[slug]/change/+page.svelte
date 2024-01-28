<script lang="ts">
	import type { MainVehicle } from '$lib/interfaces/vehicles.interface';
	export let data;
	const vehicleDetails = data;
</script>

<div class="content__card row">
	<div class="col-lg-12">
		<div class="fl-row jc-between">
			<div class="title--wrapper w-100">
				<h1 class="heading-24">Change Vehicle</h1>
				<h2 class="med-20 vehicle-spec btn-slim">{vehicleDetails.slug}</h2>
			</div>
			<div class="form-group required">
				<label for="company_name">Status</label>
				<label class="check--wrapper activity">
					<input class="check-switch" type="checkbox" bind:checked={vehicleDetails.is_active} />
				</label>
				<small class="error_text">There's a mistake there.</small>
			</div>
		</div>
	</div>
	<div class="col-6">
		<div class="form-group required">
			<label for="first_name">Vehicle Name</label>
			<input type="text" class="form-control" name="first_name" id="first_name" />
			<small class="error_text">There's a mistake there.</small>
		</div>
	</div>
	<div class="col-6">
		<div class="form-group required">
			<label for="registration_number">Vehicle Registration Number</label>
			<input
				type="text"
				class="form-control"
				name="registration_number"
				id="registration_number"
				value={vehicleDetails.reg_no}
			/>
			<small class="error_text">There's a mistake there.</small>
		</div>
	</div>
	<div class="col-2">
		<div class="form-group required">
			<label for="seats">Seats</label>
			<input type="number" class="form-control" name="seats" id="seats" />
			<small class="error_text">There's a mistake there.</small>
		</div>
	</div>
	<div class="col-4">
		<div class="form-group required">
			<label for="color_name">Vehicle Color Name</label>
			<input type="text" class="form-control" name="color_name" id="color_name" />
			<small class="error_text">There's a mistake there.</small>
		</div>
	</div>
	<div class="col-4">
		<div class="form-group required">
			<label for="color_code">Vehicle Color Code</label>
			<input type="text" class="form-control" name="color_code" id="color_code" />
			<small class="error_text">There's a mistake there.</small>
		</div>
	</div>
	<div class="col-4">
		<div class="form-group required">
			<label for="model_name">Vehicle Model Name</label>
			<input type="text" class="form-control" name="model_name" id="model_name" />
			<small class="error_text">There's a mistake there.</small>
		</div>
	</div>
	<div class="col-4">
		<div class="form-group required">
			<label for="model_manufacturer">Vehicle Model Manufacturer</label>
			<input type="text" class="form-control" name="model_manufacturer" id="model_manufacturer" />
			<small class="error_text">There's a mistake there.</small>
		</div>
	</div>
	<div class="col-3">
		<div class="form-group required">
			<label for="daily_price">Vehicle Price</label>
			<input type="text" class="form-control" name="daily_price" id="daily_price" />
			<small class="error_text">There's a mistake there.</small>
		</div>
	</div>
	<div class="col-4">
		<div class="form-group required">
			<label for="vehicle_location">Vehicle Location</label>
			<input type="text" class="form-control" name="vehicle_location" id="vehicle_location" />
			<small class="error_text">There's a mistake there.</small>
		</div>
	</div>
	<div class="col-3">
		<div class="form-group required">
			<label for="mileage">Mileage</label>
			<input type="text" class="form-control" name="mileage" id="mileage" />
			<small class="error_text">There's a mistake there.</small>
		</div>
	</div>
	<div class="col-6">
		<div class="form-group required">
			<label for="first_name">Large field</label>
			<input type="text" class="form-control large" name="first_name" id="first_name" />
			<small class="error_text">There's a mistake there.</small>
		</div>
	</div>
	<div class="col-6">
		<div class="form-group required">
			<label for="first_name">Normal Select</label>
			<select class="form-control normal" name="select__s" id="select__s">
				<option value="Happening" selected>Happenning</option>
				<option value="nothappennnig">Not Happenning</option>
			</select>
			<small class="error_text">There's a mistake there.</small>
		</div>
	</div>
	<div class="col-4">
		<div class="form-group required">
			<label for="first_name">Small Select</label>
			<select class="form-control" name="select__s" id="select__s">
				<option value="Happening" selected>Happenning</option>
				<option value="nothappennnig">Not Happenning</option>
			</select>
			<small class="error_text">There's a mistake there.</small>
		</div>
	</div>
	<div class="col-8">
		<div class="form-group required">
			<label for="first_name">Large Select</label>
			<select class="form-control" name="select__s" id="select__s">
				<option value="Happening" selected>Happenning</option>
				<option value="nothappennnig">Not Happenning</option>
			</select>
			<small class="error_text">There's a mistake there.</small>
		</div>
	</div>

	<div class="col-12">
		<div class="form-group required">
			<label for="first_name">Full Size field</label>
			<input type="text" class="form-control" name="first_name" id="first_name" />
			<small class="error_text">There's a mistake there.</small>
		</div>
	</div>
	<div class="col-6">
		<div class="form-group required">
			<label for="first_name">Select 2</label>
			<select class="form-control select-2" name="select__s" id="select__s">
				<option value="Happening" selected>Happenning</option>
				<option value="nothappennnig">Not Happenning</option>
			</select>
			<small class="error_text">There's a mistake there.</small>
		</div>
	</div>
	<div class="col-6">
		<div class="form-group">
			<label for="first_name">Input Group</label>
			<div class="input-group">
				<button data-input="thumbnail1e" data-preview="holder1e" class="lfm group-btn"
					><i class="fa fa-picture-o" /> Choose</button
				>
				<input id="thumbnail1e" class="form-control" type="text" name="image" />
			</div>
			<small class="error_text">There's a mistake there.</small>
		</div>
	</div>
	<div class="col-6">
		<div class="form-group required">
			<label for="first_name">Select 2</label>
			<div class="form-group">
				<label for="check2" class="check--label">
					<input type="checkbox" class="check--control" name="check2" id="check2" />
					<span class="check--mark" />
					Value
				</label>
			</div>
			<div class="form-group">
				<label for="check2" class="check--label">
					<input type="checkbox" class="check--control" name="check2" id="check2" />
					<span class="check--mark" />
					Value
				</label>
			</div>
			<div class="form-group">
				<label for="check2" class="check--label">
					<input type="checkbox" class="check--control" name="check2" id="check2" />
					<span class="check--mark" />
					Value
				</label>
			</div>

			<small class="error_text">There's a mistake there.</small>
		</div>
	</div>
	<div class="col-12">
		<div class="end-action-group">
			<button class="btn icon--button">
				<div class="user--label btn-label">Cancel</div>
				<div class="btn-icon">
					<span class="material-symbols-rounded"> cancel </span>
				</div>
			</button>

			<button
				class="btn icon--button btn--primary save-btn"
				data-bs-toggle="modal"
				data-bs-target="#confirmationModal"
				data-modal-mode="save"
			>
				<div class="user--label btn-label">Save</div>
				<div class="btn-icon">
					<span class="material-symbols-rounded"> save </span>
				</div>
			</button>
		</div>
	</div>
</div>
