import { expect, test } from '@playwright/test';
import { PoiComponent } from '~/playwright/models/components/poiComponent';

test.describe('Share link workflows', async () => {
  test('Open share link @regression @410', async ({ page }) => {
    await page.goto('?q=AA0284');
    let poiComponent = new PoiComponent(page);
    await expect(poiComponent.roomCode).toBeVisible();
    await expect(poiComponent.searchTitle).toBeVisible();
  });
});
