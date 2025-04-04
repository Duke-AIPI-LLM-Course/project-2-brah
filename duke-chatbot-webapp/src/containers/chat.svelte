<script>
    let { children } = $props();
</script>
<div class="chat-container flex flex-col justify-between items-center w-2/3 h-3/4 bg-black text-white rounded-lg ml-10 mr-10 mt-10 mb-10 opacity-80 z-0">
    {@render children()}
</div>
