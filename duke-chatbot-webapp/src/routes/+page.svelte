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
                <ChatMessage message="Hello, how are you?" role="user" />
                <ChatMessage message="I'm fine, thank you!" role="assistant" />
            </ChatMessageContainer>
            <ChatInput />
        </Chat>
    </Body>
    <Footer>
        <p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>
    </Footer>
</div>

