# Setup the Vue, Nuxt Frontend
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

## Customize Style
View the `/assets/custom_css` folder to find   here you can place your custom css styles


## Create production build
```
yarn run generate
```
Now just copy the `/dist` folder to your favourite webserver or static file server to serve it up using
nginx, S3, GCP cloud storage, Netlify, you name it.

## Customize style
> #### [Floor changer](assets/README.md#floor-changer)