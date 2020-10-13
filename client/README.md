# zoom-attendance-check client application

## Requirements

1.  Install nvm, yarn, node
2.  `nvm install && nvm use`
3.  `yarn`
4.  `yarn build`
5.  `yarn serve`

Now open `http://localhost:8080` and view the application!

## Project Structure

In order to separate between different parts of the application, I decided to manage this project as a monorepo and split it into modules. In order to manage the
monorepo, I decided to use [yarn workspaces](https://classic.yarnpkg.com/en/docs/workspaces/) as it's already built into yarn (as opposed to lerna, for example).

- The [`services`](./packages/services) module will handle all of the calls to outside services (both to the internal API and to external APIs).
- The [`components`](./packages/components) module holds all of the React components the project uses.
- The [`application`](./packages/application) module holds the webpack building infrastructure and different React providers (i.e. Redux providers).

Separating these into different modules, each with its own TS configuration, allows for fast build times for single artifacts and easier testing.
