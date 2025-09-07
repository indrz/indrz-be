import { expect, test } from '@playwright/test';
import { DirectionsComponent } from '~/playwright/models/components/directionsComponent';
import { HomePage } from '~/playwright/models/pages/homepage';

test.beforeEach(async ({ page }) => {
  await page.goto('/');
  let homePage = new HomePage(page);
  await expect(homePage.searchToolbar).toBeVisible();
});

test('Toggle left side pane', async ({ page }) => {
  let homePage = new HomePage(page);
  await homePage.clickToggleLeftPane();
  await expect(homePage.leftPaneComponent.sideBar).toBeVisible();
});

test('Open directions pane using directions shortcut button', async ({ page }) => {
  let homePage = new HomePage(page);
  await homePage.clickDirectionsShortcut();
  let directionsComponent = new DirectionsComponent(page);
  await expect(directionsComponent.directionsPane).toBeVisible();
});