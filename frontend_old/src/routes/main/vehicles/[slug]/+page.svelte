<script lang="ts">
	export let data;
	const vehicleDetails = data;
</script>

<div class="py-sm">
	<div class="container">
		<div class="row">
			<div class="col-lg-12">
				<a href="/" class="btn btn-global btn--grey">
					<i class="ti ti-chevron-left" /> Go Back
				</a>
			</div>
			<div class="col-lg-12">
				<header class="header__section">
					<div class="row al-stretch jc-between">
						<div class="col-12 col-lg-5">
							<div class="heading__description--wrapper">
								<h1 class="heading-3">
									{vehicleDetails.model_manufacturer}
									{vehicleDetails.model_name}
								</h1>
								<div class="vehicle__card--text-wrapper">
									<div class="vehicle__bound">
										{vehicleDetails.vehicle_location}, {vehicleDetails.vehicle_city}
									</div>
									<div class="vehicle__number primary heading-6 py-xs">
										{vehicleDetails.reg_no.toUpperCase()}
									</div>
								</div>
								<a href="/user/{vehicleDetails.vehicle_owner.id}">
									<div class="vehicle__owner my-xs">
										<div class="vehicle__owner--image">
											<img src={vehicleDetails.vehicle_image} alt="" />
										</div>
										<div class="vehicle__owner--name">{vehicleDetails.vehicle_owner.full_name}</div>
									</div>
								</a>

								<div class="price-box heading-4 my-sm">
									Rs. {parseInt(vehicleDetails.vehicle_daily_price)}
								</div>

								<div class="vehicle__card--spec-grid py-xs">
									<div class="spec-group group-row">
										<div class="spec-title">Color:</div>
										<div class="spec-value">
											<div class="color-value">
												<div class="color-circle" style="--color: #{vehicleDetails.color_code}" />
												{vehicleDetails.color_name}
											</div>
										</div>
									</div>
									<div class="spec-group group-row">
										<div class="spec-title">Seats <i class="ti ti-users" /></div>
										<div class="spec-value">{vehicleDetails.seats} Seats</div>
									</div>
									<div class="spec-group group-row">
										<div class="spec-title">Transmission <i class="ti ti-hexagon" /></div>
										<div class="spec-value">{vehicleDetails.transmission}</div>
									</div>
									<div class="spec-group group-row">
										<div class="spec-title">Mileage <i class="ti ti-hexagon" /></div>
										<div class="spec-value">{vehicleDetails.mileage}</div>
									</div>
								</div>
							</div>
						</div>
						<div class="col-12 col-lg-4">
							<div class="header__image--wrapper">
								<div class="df-image-wrapper">
									<img src={vehicleDetails.vehicle_image} alt="" />
								</div>
							</div>
							<div class="vehicle__ratings--wrapper">
								<div class="spec-row"><i class="ti ti-steering-wheel" /> 156 Drives</div>
								<div class="spec-row"><i class="ti ti-steering-wheel" /> 9000 KM Driven</div>
							</div>
							<div class="fl-row gap-2 al-center py-sm">
								<a href="/main/book/{vehicleDetails.slug}" class="btn btn-global btn--primary w-100"
									>Book Now</a
								>
							</div>
						</div>
					</div>
				</header>
				<section class="rental-information my-ms">
					<h3 class="heading-4">Rental Information</h3>
					<div class="pt-sm">
						<span class="info-title">
							<span class="heading-5">Required Items</span>
						</span>
						<div class="info-checklist py-xs">
							<div class="info-checklist--item">
								<i class="ti ti-circle-check" /> Passport or National ID Card
							</div>
							<div class="info-checklist--item">
								<i class="ti ti-circle-check" /> International / Local Driver's License
							</div>
							<div class="info-checklist--item">
								<i class="ti ti-circle-check" /> Prepaid Fee
							</div>
						</div>
					</div>
					<div class="py-sm">
						<span class="info-title">
							<span class="heading-5">Rules for Rental</span>
						</span>
						<div class="info-checklist py-xs">
							<div class="info-checklist--item">
								<span class="title">Security Deposit: </span> Rs. 10000
								<em>Refundable on Vehicle Return</em>
							</div>
							<div class="info-checklist--item">
								<span class="title">Driving Limit: </span> 500 KM
								<em>On Excess, Rs. 100 per KM will be charged</em>
							</div>
							<div class="info-checklist--item">
								<span class="title">Area Limit: </span> Within Location Bounds
							</div>
						</div>
					</div>
				</section>
			</div>
		</div>
	</div>
</div>
