import { expect, test } from '@playwright/test';
import {
  DirectionSearch,
  DirectionsComponent
} from '~/playwright/models/components/directionsComponent';
import { HomePage } from '~/playwright/models/pages/homepage';

test.beforeEach(async ({ page }) => {
  await page.goto('/');
  let homePage = new HomePage(page);
  await expect(homePage.searchToolbar).toBeVisible();
});

test('Karlsplatz from Aula to Prechtlsaal search', async ({ page }) => {
  let homePage = new HomePage(page);

  await homePage.clickToggleLeftPane();
  await homePage.leftPaneComponent.showDirections();

  let directionsCom = new DirectionsComponent(page);

  let directionSearch: DirectionSearch = {
    fromSearch: {
      searchText: 'Aula',
      searchResultId: 'AAEG06'
    },
    toSearch: {
      searchText: 'Prechtlsaal',
      searchResultId: 'AAEG18KL'
    }
  };

  await directionsCom.getDirections(directionSearch);
  await page.waitForTimeout(10000);
  await expect(homePage.mapComponent.map).toBeVisible();
  await expect(page).toHaveScreenshot('AulaToPrechtlsaal.png',{maxDiffPixelRatio: 0.05});
});
