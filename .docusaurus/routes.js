import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '5ff'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '5ba'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', 'a2b'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', 'c3c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', '156'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '88c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '000'),
    exact: true
  },
  {
    path: '/blog',
    component: ComponentCreator('/blog', 'b2f'),
    exact: true
  },
  {
    path: '/blog/archive',
    component: ComponentCreator('/blog/archive', '182'),
    exact: true
  },
  {
    path: '/blog/authors',
    component: ComponentCreator('/blog/authors', '0b7'),
    exact: true
  },
  {
    path: '/blog/authors/all-sebastien-lorber-articles',
    component: ComponentCreator('/blog/authors/all-sebastien-lorber-articles', '4a1'),
    exact: true
  },
  {
    path: '/blog/authors/yangshun',
    component: ComponentCreator('/blog/authors/yangshun', 'a68'),
    exact: true
  },
  {
    path: '/blog/first-blog-post',
    component: ComponentCreator('/blog/first-blog-post', '89a'),
    exact: true
  },
  {
    path: '/blog/long-blog-post',
    component: ComponentCreator('/blog/long-blog-post', '9ad'),
    exact: true
  },
  {
    path: '/blog/mdx-blog-post',
    component: ComponentCreator('/blog/mdx-blog-post', 'e9f'),
    exact: true
  },
  {
    path: '/blog/tags',
    component: ComponentCreator('/blog/tags', '287'),
    exact: true
  },
  {
    path: '/blog/tags/docusaurus',
    component: ComponentCreator('/blog/tags/docusaurus', '704'),
    exact: true
  },
  {
    path: '/blog/tags/facebook',
    component: ComponentCreator('/blog/tags/facebook', '858'),
    exact: true
  },
  {
    path: '/blog/tags/hello',
    component: ComponentCreator('/blog/tags/hello', '299'),
    exact: true
  },
  {
    path: '/blog/tags/hola',
    component: ComponentCreator('/blog/tags/hola', '00d'),
    exact: true
  },
  {
    path: '/blog/welcome',
    component: ComponentCreator('/blog/welcome', 'd2b'),
    exact: true
  },
  {
    path: '/markdown-page',
    component: ComponentCreator('/markdown-page', '3d7'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', 'a9f'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', 'e10'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', '62f'),
            routes: [
              {
                path: '/docs/category/examples',
                component: ComponentCreator('/docs/category/examples', '04a'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/category/tutorial---basics',
                component: ComponentCreator('/docs/category/tutorial---basics', '20e'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/category/tutorial---extras',
                component: ComponentCreator('/docs/category/tutorial---extras', '9ad'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/',
                component: ComponentCreator('/docs/classes/', '32d'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/action',
                component: ComponentCreator('/docs/classes/action', '46a'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/actionstatus',
                component: ComponentCreator('/docs/classes/actionstatus', '02f'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/actiontype',
                component: ComponentCreator('/docs/classes/actiontype', '512'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/actor',
                component: ComponentCreator('/docs/classes/actor', 'd95'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/constraint',
                component: ComponentCreator('/docs/classes/constraint', '895'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/conveyor',
                component: ComponentCreator('/docs/classes/conveyor', 'a8d'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/job',
                component: ComponentCreator('/docs/classes/job', 'd34'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/jobpriority',
                component: ComponentCreator('/docs/classes/jobpriority', 'a31'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/jobstatus',
                component: ComponentCreator('/docs/classes/jobstatus', '325'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/location',
                component: ComponentCreator('/docs/classes/location', 'ab3'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/locationtype',
                component: ComponentCreator('/docs/classes/locationtype', 'edc'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/machine',
                component: ComponentCreator('/docs/classes/machine', 'f1c'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/part',
                component: ComponentCreator('/docs/classes/part', '11d'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/parttype',
                component: ComponentCreator('/docs/classes/parttype', '7ec'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/product',
                component: ComponentCreator('/docs/classes/product', '5a8'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/productionstate',
                component: ComponentCreator('/docs/classes/productionstate', 'db9'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/requirement',
                component: ComponentCreator('/docs/classes/requirement', 'd90'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/requirementtype',
                component: ComponentCreator('/docs/classes/requirementtype', '65d'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/resource',
                component: ComponentCreator('/docs/classes/resource', '68c'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/resourcestatus',
                component: ComponentCreator('/docs/classes/resourcestatus', '5e4'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/resourcetype',
                component: ComponentCreator('/docs/classes/resourcetype', 'c6c'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/roboticarm',
                component: ComponentCreator('/docs/classes/roboticarm', '355'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/route',
                component: ComponentCreator('/docs/classes/route', 'bc8'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/sensor',
                component: ComponentCreator('/docs/classes/sensor', '92a'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/storage',
                component: ComponentCreator('/docs/classes/storage', 'a6d'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/storagetype',
                component: ComponentCreator('/docs/classes/storagetype', '51b'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/tool',
                component: ComponentCreator('/docs/classes/tool', '61b'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/vehicle',
                component: ComponentCreator('/docs/classes/vehicle', 'f4f'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/vehicletype',
                component: ComponentCreator('/docs/classes/vehicletype', 'f75'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/worker',
                component: ComponentCreator('/docs/classes/worker', '8df'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/classes/workstation',
                component: ComponentCreator('/docs/classes/workstation', '3a6'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/examples/3d-printing-factory',
                component: ComponentCreator('/docs/examples/3d-printing-factory', 'c6f'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/getting_started',
                component: ComponentCreator('/docs/getting_started', '4f4'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/intro',
                component: ComponentCreator('/docs/intro', '61d'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/tutorial-basics/congratulations',
                component: ComponentCreator('/docs/tutorial-basics/congratulations', '458'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/tutorial-basics/create-a-blog-post',
                component: ComponentCreator('/docs/tutorial-basics/create-a-blog-post', '108'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/tutorial-basics/create-a-document',
                component: ComponentCreator('/docs/tutorial-basics/create-a-document', '8fc'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/tutorial-basics/create-a-page',
                component: ComponentCreator('/docs/tutorial-basics/create-a-page', '951'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/tutorial-basics/deploy-your-site',
                component: ComponentCreator('/docs/tutorial-basics/deploy-your-site', '4f5'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/tutorial-basics/markdown-features',
                component: ComponentCreator('/docs/tutorial-basics/markdown-features', 'b05'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/tutorial-extras/manage-docs-versions',
                component: ComponentCreator('/docs/tutorial-extras/manage-docs-versions', '978'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/tutorial-extras/translate-your-site',
                component: ComponentCreator('/docs/tutorial-extras/translate-your-site', 'f9a'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', 'e5f'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
