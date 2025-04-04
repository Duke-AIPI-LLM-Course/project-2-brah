<script>
    import { Icon, User, AcademicCap } from 'svelte-hero-icons'
    let { message, role } = $props();
    let flexDirection = role === 'user' ? 'flex-row-reverse' : 'flex-row';
    let textAlign = role === 'user' ? 'text-right' : 'text-left';
    let justify = role === 'user' ? 'justify-end' : 'justify-start';
    let bgColor = role === 'user' ? 'bg-blue-500' : 'bg-gray-500';
    let icon = role === 'user' ? User : AcademicCap;
</script>
<div class="chat-message flex {flexDirection} items-center z-10">
    <Icon src={icon} class="w-10 h-10 text-white pl-1 pr-1" solid />
    <div class="chat-message-content {bgColor} p-2 rounded-lg max-w-2/3 flex-wrap">
        <p class="chat-message-content-user {textAlign} {justify}">{message}</p>
    </div>
</div>
