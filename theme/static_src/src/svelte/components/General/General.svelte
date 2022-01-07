<script lang="ts">
	import { onMount } from 'svelte';
	import { fade, fly } from 'svelte/transition';
	import { UserStore, UIStore, UpdatesStore } from '../../store/index';
	import type { ICity, ICountry, IProfile } from '../../types/models';
	import CancelButton from '../shared/CancelButton.svelte';
	import Card from '../shared/Card.svelte';
	import FormInput from '../shared/FormInput.svelte';
	import SuccessNotifier from '../shared/SuccessNotifier.svelte';
	import ErrorNotifier from '../shared/ErrorNotifier.svelte';
	import UpdateButton from '../shared/UpdateButton.svelte';
	import TabView from '../shared/TabView.svelte';
	import FormSelect from '../shared/FormSelect.svelte';

	export let model: IProfile;
	export let countries: ICountry[];
	export let cities: ICity[];
	export let errors;
	let tabs = [{ name: 'Base' }, { name: 'Updates' }];
	let tabName = tabs[0].name;

	$: UIData = $UIStore;
	$: updatesData = $UpdatesStore;
	$: updateNotEmpty = Object.keys(updatesData.model).length;

	const scrollUpToSuccessMessage = () => {
		// Show a success message
		window.scrollTo(0, 0);
		// TODO(karim): find what condition implies success
		// if (UIData.success) {
		//   // Hide the success message after 2 seconds
		//   setTimeout(() => {
		//     UIStore.setFeedbackModal(false);
		//   }, 2000);
		// }
	};

	const onValueChanged = ({ detail }) => {
		model[detail.name] = detail.value;
	};

	const onUpdateValueChanged = ({ detail }) => {
		updatesData.model[detail.name] = detail.value;
	};

	const onlyAdd = (...fields: string[]) => {
		const payload = { id: model.id };

		fields.forEach((field) => {
			if (model[field] != undefined) payload[field] = model[field];
		});

		return payload;
	};

	const handleSubmit = async (payloadType: string) => {
		let payload = {};

		switch (payloadType.toLowerCase()) {
			case 'profile':
				payload = onlyAdd(
					'first_name',
					'last_name',
					'phone',
					'birth_date',
					'gender',
					'nin'
				);
				break;
			case 'location':
				payload = onlyAdd('country', 'city', 'address', 'zipcode');
				break;
			case 'online':
				payload = onlyAdd('facebook', 'instagram');
				break;
			default:
				payload = model;
		}

		await UserStore.updateModel(payload);

		// Show a success message
		scrollUpToSuccessMessage();
		// TODO(karim): find what condition implies success
		// if (UIData.success) {
		//   // Hide the success message after 2 seconds
		//   setTimeout(() => {
		//     UIStore.setFeedbackModal(false);
		//   }, 2000);
		// }
	};

	const createBioUpdate = async () => {
		await UpdatesStore.createProfileUpdate(model.bio);

		scrollUpToSuccessMessage();
	};

	const modifyUpdateRequest = async () => {
		const { model: modelUpdate } = updatesData;
		await UpdatesStore.modifyProfileUpdate(modelUpdate.id, modelUpdate);

		scrollUpToSuccessMessage();
	};

	const removeUpdateRequest = async () => {
		await UpdatesStore.deleteProfileUpdate(updatesData.model.id);

		scrollUpToSuccessMessage();
	};

	onMount(async () => {
		// Get user updates
		if (!updateNotEmpty) {
			UpdatesStore.getProfileUpdate();
		}

		if (!countries.length) {
			await UserStore.getCountries();

			if (!cities.length) {
				const countryField = document.querySelector<HTMLSelectElement>(
					'#country'
				);
				const { options, selectedIndex } = countryField;
				const { text, value } = options[selectedIndex];

				await UserStore.getCities(text, value);
			}
		}
	});
</script>

<TabView {tabs} {tabName} on:change={({ detail }) => (tabName = detail)} />

<SuccessNotifier />

{#if tabName === tabs[0].name}
	<div in:fly={{ x: -200, duration: 400 }} out:fade={{ duration: 100 }}>
		<Card title="Edit Profile">
			<form on:submit|preventDefault={handleSubmit.bind(this, 'profile')}>
				<div class="sm:flex sm:justify-center">
					<div class="w-full">
						<FormInput
							value={model.first_name}
							name="first_name"
							label="Nom"
							errors={errors['first_name']}
							on:valueChanged={onValueChanged} />
						<FormInput
							value={model.last_name}
							name="last_name"
							label="Prenom"
							errors={errors['last_name']}
							on:valueChanged={onValueChanged} />
						<FormInput
							value={model.phone}
							name="phone"
							label="Phone"
							errors={errors['phone']}
							on:valueChanged={onValueChanged} />
					</div>
					<div class="w-full mt-4 sm:mt-0 sm:ml-4">
						<FormInput
							value={model.birth_date}
							name="birth_date"
							label="Date de Niassance"
							errors={errors['birth_date']}
							on:valueChanged={onValueChanged} />
						<FormInput
							value={model.gender}
							type="select"
							selectOptions={['f', 'm']}
							name="gender"
							label="Sexe"
							errors={errors['gender']}
							on:valueChanged={onValueChanged} />
						<FormInput
							value={model.nin}
							name="nin"
							label="CIN"
							errors={errors['nin']}
							on:valueChanged={onValueChanged} />
					</div>
				</div>
				<div class="text-right mt-2 sm:mt-4">
					<UpdateButton fetching={UIData.fetching} />
				</div>
			</form>
		</Card>

		<ErrorNotifier
			errors={updatesData.errors}
			errorKey="model"
			on:clearErrors={() => UpdatesStore.clearErrors('model')} />
		<Card
			title="About Me"
			description="This section must be filled in order to make your profile
      public.">
			<form on:submit|preventDefault={createBioUpdate}>
				<FormInput
					value={model.bio}
					type="textarea"
					name="bio"
					label="Bio"
					errors={updatesData.errors.bio}
					on:valueChanged={onValueChanged} />
				<div class="text-right mt-2 sm:mt-4">
					<UpdateButton fetching={UIData.fetching} />
				</div>
			</form>
		</Card>

		<Card title="Location">
			<form on:submit|preventDefault={handleSubmit.bind(this, 'location')}>
				<div class="sm:flex sm:justify-center">
					<div class="w-full">
						<FormSelect
							name="country"
							label="Pays"
							value={model.country}
							optionValue="code"
							optionText="name"
							selectOptions={countries}
							on:valueChanged={onValueChanged}
							errors={errors['country']} />
						<FormInput
							value={model.address}
							name="address"
							label="Adresse"
							errors={errors['address']}
							on:valueChanged={onValueChanged} />
					</div>
					<div class="w-full mt-4 sm:mt-0 sm:ml-4">
						<FormSelect
							name="city"
							label="Ville"
							value={model.city}
							optionValue="name"
							optionText="name"
							selectOptions={cities}
							on:valueChanged={onValueChanged}
							errors={errors['city']} />
						<FormInput
							value={model.zipcode}
							type="number"
							name="zipcode"
							label="Code Postal"
							errors={errors['zipcode']}
							on:valueChanged={onValueChanged} />
					</div>
				</div>
				<div class="text-right mt-2 sm:mt-4">
					<UpdateButton fetching={UIData.fetching} />
				</div>
			</form>
		</Card>

		<Card title="Online Presence">
			<form on:submit|preventDefault={handleSubmit.bind(this, 'online')}>
				<div class="sm:flex sm:justify-center">
					<div class="w-full">
						<FormInput
							value={model.facebook}
							name="facebook"
							label="Facebook"
							errors={errors['facebook']}
							on:valueChanged={onValueChanged} />
					</div>
					<div class="w-full mt-4 sm:mt-0 sm:ml-4">
						<FormInput
							value={model.instagram}
							name="instagram"
							label="Instagram"
							errors={errors['instagram']}
							on:valueChanged={onValueChanged} />
					</div>
				</div>
				<div class="text-right mt-2 sm:mt-4">
					<UpdateButton fetching={UIData.fetching} />
				</div>
			</form>
		</Card>
	</div>
{:else if tabName === tabs[1].name}
	<div in:fly={{ x: -200, duration: 400 }} out:fade={{ duration: 100 }}>
		{#if updateNotEmpty}
			<ErrorNotifier
				errors={updatesData.model.errors}
				errorKey="model"
				on:clearErrors={UpdatesStore.clearProfileUpdateErrors} />
			{#if updatesData.model.message.length}
				<Card
					classes={updatesData.model.accept ? 'border-green-300' : 'border-red-300'}>
					<h1 class="text-lg font-semibold">Response</h1>
					<p class="mt-2 text-sm text-gray-800">{updatesData.model.message}</p>
				</Card>
			{/if}
			<Card classes="mb-4">
				<form on:submit|preventDefault={modifyUpdateRequest}>
					<FormInput
						value={updatesData.model.bio}
						type="textarea"
						name="bio"
						label="Bio"
						errors={updatesData.model?.errors['bio']}
						on:valueChanged={onUpdateValueChanged} />

					<div class="flex justify-end items-center mt-2 space-x-4">
						<CancelButton
							text="Remove"
							fetching={UIData.fetching}
							on:click={removeUpdateRequest} />
						<UpdateButton type="submit" fetching={UIData.fetching} />
					</div>
				</form>
			</Card>
		{:else}
			<p class="mt-6 text-gray-700">No Updates</p>
		{/if}
	</div>
{/if}
