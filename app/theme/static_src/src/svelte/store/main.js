import { writable } from 'svelte/store'
import { isOnline } from "../../main/utils";

export async function createModelStore() {
	let data;
	await isOnline(async () => {
		data = await (await fetch('/api/models/me')).json()
	})
	const modelData = data && JSON.parse(data.model)
    const model = modelData ? {id: modelData[0].pk , ...modelData[0].fields, email: data.email} : {}

	const { subscribe, set, update } = writable(model);

	return {
		subscribe,
		update,
		set,
		// increment: () => update(n => n + 1),
		// decrement: () => update(n => n - 1),
		reset: () => set({})
	};
}