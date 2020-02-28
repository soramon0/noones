import { writable } from 'svelte/store'

export async function createModelStore() {
    const data = await (await fetch('/api/models/me')).json()
	const modelData = JSON.parse(data.model)
    const model = {id: modelData[0].pk , ...modelData[0].fields, email: data.email}

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