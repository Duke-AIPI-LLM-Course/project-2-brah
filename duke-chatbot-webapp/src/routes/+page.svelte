<script>
    import Duke100 from '../components/duke100.svelte';
    import Header from '../containers/header.svelte';
    import HeaderRow from '../containers/headerRow.svelte';
    import Body from '../containers/body.svelte';
    import Footer from '../containers/footer.svelte';
    import TitleContainer from '../containers/titleContainer.svelte';
    import Chat from '../containers/chat.svelte';
    import ChatMessageContainer from '../containers/chatMessageContainer.svelte';
	import ChatInput from '../components/chatInput.svelte';
    import ChatMessage from '../components/chatMessage.svelte';
    import Logo from '../components/logo.svelte';

    import { v4 as uuidv4 } from 'uuid';

    let messages = $state([]);
    let messageNumber = $state(0);
    let loading = $state(false);

    async function sendUserMessage(message) {
        loading = true;
        messages = [{
            role: 'user',
            content: message,
            id: uuidv4(),
        }, ...messages];
        let response = await fetch('/completions', {
            method: 'POST',
            body: JSON.stringify({ messages }),
        });
        let data = await response.json();
        messages = data.messages;
        loading = false;
    }
</script>
<div class="flex flex-col h-screen justify-between">
    <Header>
        <Duke100 />
        <HeaderRow>
            <TitleContainer>
                <Logo />
                <h1>Chatbot</h1>
            </TitleContainer>
        </HeaderRow>
    </Header>
    <Body>
        <Chat>
            <ChatMessageContainer>
                {#each messages as message (message.id)}
                    <ChatMessage message={message.content} role={message.role} />
                {/each}
            </ChatMessageContainer>
            <ChatInput onSend={sendUserMessage} loading={loading} />
        </Chat>
    </Body>
    <Footer>
        <p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>
    </Footer>
</div>
