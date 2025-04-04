<script>
    let { children } = $props();
</script>
<div class="chat-message-container flex flex-col-reverse w-3/4 h-7/8 mt-5 mb-5 overflow-auto">
    {@render children()}
</div>
