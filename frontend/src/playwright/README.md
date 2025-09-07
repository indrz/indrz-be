Playwright is being used as the frontend API & UI testing framework. This allows us to test multiple browsers and devices in parallel. 

## Setup
1. Clone down the frontend repository
2. Open the repo in terminal
3. Install the required browser drivers using the command
`yarn playwright install`

## VS Code extension
If you're using VS Code it's extremely recommended you down the playwright extension. This will allow you to easily debug tests from the test explorer pane.
https://playwright.dev/docs/running-tests#run-tests-in-vs-code
https://marketplace.visualstudio.com/items?itemName=ms-playwright.playwright

## Running the tests
To run all the API & UI tests, run the following command:
`
yarn pw:test
`
You can also filter tests when running the command, see this page for the filter syntax.
i.e. Only run tests in share.spec.ts 
`
npx playwright test share.spec.ts
`
https://playwright.dev/docs/test-cli


## API Tests
coming soon

## UI Tests
The UI tests have been written using POM(Page object model) structure. This allows us to re-use pages/components across the test suite.
For more information on playwright/POM see https://playwright.dev/docs/pom

### Adding new baseline image verifications
When adding new baseline images for tests that perform image comparison it's important that you generate baseline images for the Linux operating system. 
This is because the CI/CD pipeline agents will always run on Linux. 
Depending on the operation system UI elements will render text and other elements differently.
See: https://playwright.dev/docs/test-snapshots 

Generating baseline images for linux
1. Ensure that the new image comparison tests are passing locally on your machine
2. Run the playwright docker container & generate baseline images
`
docker run --rm --network host -v $(pwd):/work/ -w /work/ -it mcr.microsoft.com/playwright:v1.40.0-jammy /bin/bash
npm install
npx playwright test --update-snapshots
`
3. After the tests complete the linux baseline images should be in your **-snapshots/ folder.



## CI/CD pipeline information
After a pipeline run is completed the playwright artifacts will be uploaded to the job. 
This allows you to download and debug/review failed tests.
To learn more https://playwright.dev/docs/trace-viewer-intro

Steps:
1. Navigate to the ui-test job that's completed
i.e. https://gitlab.com/indrz/indrz-frontend/-/jobs/5714693649
2. On the right-hand side click 'download' under job artifacts
3.  extract the zip contents
4. Navigate to https://trace.playwright.dev/
5. Browse to the one of the .zip files from the data folder.
i.e. ../playwright-report/3123313131324.zip
6. Trace view report will show you the history of the test(s) and why it failed

