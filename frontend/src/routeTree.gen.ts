/* eslint-disable */

// @ts-nocheck

// noinspection JSUnusedGlobalSymbols

// This file was automatically generated by TanStack Router.
// You should NOT make any changes in this file as it will be overwritten.
// Additionally, you should also exclude this file from your linter and/or formatter to prevent it from being checked or modified.

// Import Routes

import { Route as rootRoute } from './routes/__root';
import { Route as DemoImport } from './routes/demo';
import { Route as IndexImport } from './routes/index';

// Create/Update Routes

const DemoRoute = DemoImport.update({
  id: '/demo',
  path: '/demo',
  getParentRoute: () => rootRoute,
} as any);

const IndexRoute = IndexImport.update({
  id: '/',
  path: '/',
  getParentRoute: () => rootRoute,
} as any);

// Populate the FileRoutesByPath interface

declare module '@tanstack/react-router' {
  interface FileRoutesByPath {
    '/': {
      id: '/';
      path: '/';
      fullPath: '/';
      preLoaderRoute: typeof IndexImport;
      parentRoute: typeof rootRoute;
    };
    '/demo': {
      id: '/demo';
      path: '/demo';
      fullPath: '/demo';
      preLoaderRoute: typeof DemoImport;
      parentRoute: typeof rootRoute;
    };
  }
}

// Create and export the route tree

export interface FileRoutesByFullPath {
  '/': typeof IndexRoute;
  '/demo': typeof DemoRoute;
}

export interface FileRoutesByTo {
  '/': typeof IndexRoute;
  '/demo': typeof DemoRoute;
}

export interface FileRoutesById {
  __root__: typeof rootRoute;
  '/': typeof IndexRoute;
  '/demo': typeof DemoRoute;
}

export interface FileRouteTypes {
  fileRoutesByFullPath: FileRoutesByFullPath;
  fullPaths: '/' | '/demo';
  fileRoutesByTo: FileRoutesByTo;
  to: '/' | '/demo';
  id: '__root__' | '/' | '/demo';
  fileRoutesById: FileRoutesById;
}

export interface RootRouteChildren {
  IndexRoute: typeof IndexRoute;
  DemoRoute: typeof DemoRoute;
}

const rootRouteChildren: RootRouteChildren = {
  IndexRoute: IndexRoute,
  DemoRoute: DemoRoute,
};

export const routeTree = rootRoute
  ._addFileChildren(rootRouteChildren)
  ._addFileTypes<FileRouteTypes>();

/* ROUTE_MANIFEST_START
{
  "routes": {
    "__root__": {
      "filePath": "__root.tsx",
      "children": [
        "/",
        "/demo"
      ]
    },
    "/": {
      "filePath": "index.tsx"
    },
    "/demo": {
      "filePath": "demo.tsx"
    }
  }
}
ROUTE_MANIFEST_END */
