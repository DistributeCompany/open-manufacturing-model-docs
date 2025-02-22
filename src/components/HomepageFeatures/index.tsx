import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Universal Understanding',
    Svg: require('@site/static/img/undraw_informed-decision_2jwi.svg').default,
    description: (
      <>
      Bridge the gap between machines, software, and people with OMM's standardized manufacturing vocabulary.
      </>
    ),
  },
  {
    title: 'Digital Twin Ready',
    Svg: require('@site/static/img/undraw_pair-programming_9jyg.svg').default,
    description: (
      <>
      Track, monitor, and optimize your entire manufacturing process in real-time with detailed insights into every operation.
      </>
    ),
  },
  {
    title: 'Fits Any Purpose',
    Svg: require('@site/static/img/undraw_factory_4d61.svg').default,
    description: (
      <>
        Extend or customize Open Manufacturing Model to fit your use case. Integrate
        with the Open Trip Model to create an end-to-end supply chain.
      </>
    ),
  },
];

function Feature({title, Svg, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
