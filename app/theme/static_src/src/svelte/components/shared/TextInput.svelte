<script>
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();
    export let value = ''
    export let type = 'text'
    export let name
    export let label

    const valueChanged = (e) => {
        value = e.target.value
        value = type === 'number' ? +value : value
        dispatch("valueChanged", {name, value});
    }
</script>

<label for={name} class="block my-1 text-sm text-gray-700 font-semibold">{label}</label>
<input id={name} {type} {value} on:change={valueChanged} class="form-input text-gray-600 font-semibold" />