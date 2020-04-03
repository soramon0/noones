<script>
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();
    export let value = ''
    export let type = 'text'
    export let name
    export let label
    export let errors

    const valueChanged = (e) => {
        value = e.target.value
        value = type === 'number' ? +value : value
        dispatch("valueChanged", {name, value});
    }
</script>

<label for={name} class="block my-1 text-sm text-gray-700 font-semibold">{label}</label>
<input id={name} {type} {value} step={type === 'number' ? ".01" : null}  on:change={valueChanged} class="form-input text-gray-800 font-mono" />
{#if errors}
    <div>
        {#each errors as error}
            <p class="text-sm my-1 text-red-400">{error}</p>
        {/each}
    </div>
{/if}