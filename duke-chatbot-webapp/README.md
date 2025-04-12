# Duke AIPI590 Chatbot Web Application

A Svelte-based frontend application for the Duke AIPI590 Chatbot project.

## Deployment

The application is deployed at: https://duke-aipi590-brah.vercel.app/

## Environment Setup

1. Create a `.env` file in the root directory of the project
2. Copy the contents from `.env.example` and update the values as needed
3. Required environment variables:
   - `API_BASE_URL`: The URL of the backend API service (default: http://localhost:8000)

## Development

Once you've created a project and installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://svelte.dev/docs/kit/adapters) for your target environment.
