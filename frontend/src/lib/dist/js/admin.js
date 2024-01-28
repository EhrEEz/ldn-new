// // import '../node_modules/select2/dist/css/select2.min.css';
// import jQuery from 'jquery';
// import { Modal } from 'bootstrap';
// import { onMount } from 'svelte';
// import { browser } from '$app/environment';
// const confirmationModalContent = {
// 	save: {
// 		title: 'Are you sure you want to save?',
// 		body: 'Click on save changes if you are sure you want to save changes and publish.',
// 		cancel: 'No, Cancel',
// 		confirm: 'Yes, Save Changes',
// 		color_class: 'success',
// 		material_label: 'check'
// 	},
// 	delete: {
// 		title: 'Are you sure you want to delete',
// 		body: 'Click on delete, if you want to delete changes.',
// 		cancel: 'No, Cancel',
// 		confirm: 'Yes, delete',
// 		color_class: 'error',
// 		material_label: 'close'
// 	}
// };
// onMount(() => {
// 	window.jQuery = jQuery;
// 	jQuery(document).ready(function () {
// 		jQuery('[data-toggle-list]').on('click', function () {
// 			jQuery('[data-toggle-parent]').removeClass('[data-toggle-parent]');
// 			jQuery(this).parents('[data-toggle-parent]').toggleClass('active');
// 		});
// 		jQuery(document).on('click', function (event) {
// 			if (
// 				!jQuery(event.target).is('[data-toggle-parent]') &&
// 				jQuery(event.target).parents('[data-toggle-parent]').length === 0
// 			) {
// 				if (jQuery('[data-toggle-parent]').find('.active').length <= 0) {
// 					jQuery('[data-toggle-parent]').removeClass('active');
// 				}
// 			}
// 		});
// 		const confirmModal = document.getElementById('confirmationModal');
// 		confirmModal.addEventListener('show.bs.modal', function (event) {
// 			const source = jQuery(event.relatedTarget);
// 			const mode = source.data('modal-mode');
// 			const content = confirmationModalContent[`jQuery{mode}`];
// 			jQuery(this).attr('data-color-class', content.color_class);
// 			jQuery('#confimationModalContent').text(content.body);
// 			jQuery('#confirmationModalConfirm').text(content.confirm);
// 			jQuery('#confirmationModalConfirm').addClass(content.color_class);
// 			jQuery('#confirmationModalCancel').text(content.cancel);
// 			jQuery('#confirmationModalLabel').text(content.title);
// 			jQuery('#confirmationColorMode').addClass(content.color_class);
// 			jQuery('#confirmationColorMode .material-symbols-rounded').text(content.material_label);
// 		});
// 		confirmModal.addEventListener('hidden.bs.modal', function (event) {
// 			const content = jQuery(this).data('color-class');
// 			jQuery('#confimationModalContent').text('');
// 			jQuery('#confirmationModalConfirm').text('');
// 			jQuery('#confirmationModalCancel').text('');
// 			jQuery('#confirmationModalLabel').text('');
// 			jQuery('#confirmationColorMode').removeClass(`jQuery{content}`);
// 			jQuery('#confirmationModalConfirm').removeClass(`jQuery{content}`);
// 			jQuery('#confirmationColorMode .material-symbols-rounded').text('');
// 		});
// 		jQuery(document).on('change', '[data-check-main] .check--control', function () {
// 			if (jQuery(this).is(':checked')) {
// 				jQuery(this).parents('.check--group').find("input[type='checkbox']").prop('checked', true);
// 			} else {
// 				jQuery(this).parents('.check--group').find("input[type='checkbox']").prop('checked', false);
// 			}
// 		});
// 	});
// });

// // let table = new DataTable('.dataTable', {
// // 	rowReorder: {
// // 		selector: ':last-child'
// // 	},
// // 	responsive: true
// // });

// // jQuery(document).ready(function () {
// // 	showToastMessage(
// // 		"success",
// // 		{
// // 			title: "Something went wrong",
// // 			message: "hasdf ;lkasdjf; klsjdf;kjdhf khasdfhlkjsdhf; hskdfaskdfhks.",
// // 		},
// // 		3000
// // 	);
// // });

// const toastModeOptions = {
// 	success: 'check',
// 	error: 'close'
// };

// function showToastMessage(mode, options, time = 0) {
// 	const toast = jQuery('#messageToast');
// 	const toastTitle = toast.find('.toast--title');
// 	const toastDescription = toast.find('.toast--description');
// 	const toastMode = toast.attr('data-toast-mode', mode);
// 	toastMode.attr('data-toast-mode', mode);
// 	const toastIconWrapper = toast.find('.circle--wrapper');
// 	const toastIcon = toastIconWrapper.find('.material-symbols-rounded');
// 	toastIcon.text(toastModeOptions[`jQuery{mode}`]);
// 	toastTitle.text(options.title);
// 	toastDescription.text(options.message);
// 	toastIconWrapper.addClass(mode);
// 	setTimeout(() => {
// 		toast.addClass('show');
// 	}, 300);
// 	if (time !== 0) {
// 		setTimeout(() => {
// 			toast.removeClass('show');
// 			setTimeout(() => {
// 				toastIcon.text('');
// 				toastTitle.text('');
// 				toastDescription.text('');
// 				toastIconWrapper.removeClass(mode);
// 			}, 300);
// 		}, time);
// 	}
// 	jQuery('.toast--dismiss').on('click', function () {
// 		toast.removeClass('show');
// 		setTimeout(() => {
// 			toastIcon.text('');
// 			toastTitle.text('');
// 			toastDescription.text('');
// 			toastIconWrapper.removeClass(mode);
// 		}, 300);
// 	});
// }
