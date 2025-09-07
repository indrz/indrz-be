import { Locator, Page, expect } from '@playwright/test';

export class MapComponent {
  private page: Page;
  map: Locator;

  constructor(page: Page) {
    this.page = page;
    this.map = this.page.getByTestId('map');
  }
}
