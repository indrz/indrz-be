# INDRZ Frontend
[Gitlab](https://gitlab.com/indrz/indrz-frontend) hosts the main repo 
Mirror repo is at [Github](https://github.com/indrz/indrz-fe)

----------------------

This is the [indrz](https://www.indrz.com) FRONTEND repository. You can find our 
documentation project here [indrz Docs](https://gitlab.com/indrz/indrz-doc) in the folder content

----------------------
> Indrz is a web application for indoor wayfinding, mapping and routing. The platform is for example used by a University that wants to provide its guests, staff and students a web map platform to allow them to find anything on campus.

## Quick setup for development
The running frontend code is of no real use without it's best friend the
[BACKEND API](https://gitlab.com/indrz/indrz-backend). Head over to get it
started.

1. Clone the repo ``git clone https://gitlab.com/indrz/indrz-frontend.git``
1. ``yarn install``
1. ``yarn run dev``

If you have issues with your install these three little steps usually help
```bash
rm -rf node_modules
rm yarn.lock
yarn cache clean
yarn install
```

## Git Commit Guide
1. Create a branch from `main`
1. Name the branch like `123-add-red-button` where it starts with the issue number then a short name no spaces uses a `-`
1. Commit small and often to your new branch, it helps for Quick code-reviews. Commit messages 
1. Create a merge request to `main` and reference the issue.


## Customize Style
View the `/assets/custom_css` folder to find   here you can place your custom css styles


## Create production build
```
yarn generate
```

To bump the version number run any of the following commands:

### To bump the major version
```
yarn generate.major
```

### To bump the minor version
```
yarn generate.minor
```

### To bump the patch version
```
yarn generate.patch
```

Now just copy the `/dist` folder to your favourite webserver or static file server to serve it up using
nginx, S3, GCP cloud storage, Netlify, you name it.
## Customize style
> #### [Floor changer](assets/README.md#floor-changer)


## Run app using docker
1. ```bash
   yarn docker-build
   ```
   And then,

1. ```bash
   yarn docker-run
   ```


## Playwright Setup
1. Install Playwright Browsers
  ```bash
  yarn create playwright
  ``` 
2. Run playwright UI tests
  ```bash
  yarn run pw:test
  ```
3. Optional: Install Playwright VS Code extension for test debugging and trace viewer
