import { Locator, Page } from '@playwright/test';

export class PoiComponent {
  private page: Page;
  poiLeftPane: Locator;
  searchTitle: Locator;
  roomCode: Locator;

  constructor(page: Page) {
    this.page = page;
    this.poiLeftPane = this.page.getByTestId('goButton');
    this.searchTitle = this.page.getByTestId('searchTitle');
    this.roomCode = this.page.getByTestId('roomCode');
  }
}
