<script>
    import { Icon, PaperAirplane } from 'svelte-hero-icons';

    let { onSend, loading } = $props();

    let message = $state('');

    async function handleSubmit(event) {
        const messageToSend = message;
        message = '';
        await onSend(messageToSend);
    }

    function handleInput(event) {
        message = event.target.value;
    }
</script>
<form class="flex flex-row w-full p-2 bg-gray-800 text-white rounded-lg" onsubmit={handleSubmit}>
    <input disabled={loading} type="text" class="w-full p-2 bg-gray-800 text-white rounded-lg" bind:value={message} oninput={handleInput} />
    <button type="submit"><Icon src={PaperAirplane} class="w-6 h-6 pl-2" /></button>
</form>
