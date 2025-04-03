<script>
    let { children } = $props();
</script>
<div class="title-container flex flex-row justify-inline items-center text-3xl">
    {@render children()}
</div>
